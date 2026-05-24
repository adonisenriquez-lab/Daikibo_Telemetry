from __future__ import annotations

import argparse
import json
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import pandas as pd


LOGGER = logging.getLogger("daikibo.telemetry")


@dataclass(frozen=True)
class SensorSpec:
    sensor_id: str
    filename: str
    metric: str
    unit: str
    sampling_rate_hz: int

    @property
    def expected_samples(self) -> int:
        return self.sampling_rate_hz * 60


UCI_SENSOR_SPECS: tuple[SensorSpec, ...] = (
    SensorSpec("PS1", "PS1.txt", "pressure", "bar", 100),
    SensorSpec("PS2", "PS2.txt", "pressure", "bar", 100),
    SensorSpec("PS3", "PS3.txt", "pressure", "bar", 100),
    SensorSpec("PS4", "PS4.txt", "pressure", "bar", 100),
    SensorSpec("PS5", "PS5.txt", "pressure", "bar", 100),
    SensorSpec("PS6", "PS6.txt", "pressure", "bar", 100),
    SensorSpec("EPS1", "EPS1.txt", "motor_power", "W", 100),
    SensorSpec("FS1", "FS1.txt", "volume_flow", "l/min", 10),
    SensorSpec("FS2", "FS2.txt", "volume_flow", "l/min", 10),
    SensorSpec("TS1", "TS1.txt", "temperature", "C", 1),
    SensorSpec("TS2", "TS2.txt", "temperature", "C", 1),
    SensorSpec("TS3", "TS3.txt", "temperature", "C", 1),
    SensorSpec("TS4", "TS4.txt", "temperature", "C", 1),
    SensorSpec("VS1", "VS1.txt", "vibration", "mm/s", 1),
    SensorSpec("CE", "CE.txt", "cooling_efficiency", "%", 1),
    SensorSpec("CP", "CP.txt", "cooling_power", "kW", 1),
    SensorSpec("SE", "SE.txt", "efficiency_factor", "%", 1),
)


class TelemetryProcessor:
    """Sprint 1 processor for cycle-based industrial telemetry.

    The UCI dataset stores one 60-second operating cycle per row. Sensors have
    different sampling rates, so the processor summarizes each sensor by cycle
    instead of resampling low-frequency sensors into invented high-frequency
    points.
    """

    def __init__(
        self,
        raw_dir: Path,
        output_dir: Path,
        base_timestamp: datetime | None = None,
        ttl_seconds: int = 300,
    ) -> None:
        self.raw_dir = Path(raw_dir)
        self.output_dir = Path(output_dir)
        self.base_timestamp = base_timestamp or datetime(2026, 1, 1, tzinfo=timezone.utc)
        self.ttl_seconds = ttl_seconds

    def run_uci_sprint1(self, max_cycles: int | None = None) -> dict[str, Any]:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        LOGGER.info("Starting UCI Sprint 1 pipeline")

        profile = self._load_profile(max_cycles=max_cycles)
        features = self.normalize(max_cycles=max_cycles)
        unified = profile.merge(features, on="cycle_id", how="left")
        unified = self.validate_quality(unified)
        events = self.generate_candidate_events(unified)
        summary = self.build_summary(unified, events)

        features_path = self.output_dir / "uci_cycle_features.csv"
        events_path = self.output_dir / "sap_candidate_events.json"
        summary_path = self.output_dir / "quality_report.json"

        unified.to_csv(features_path, index=False)
        events_path.write_text(json.dumps(events, indent=2), encoding="utf-8")
        summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

        LOGGER.info("Wrote %s", features_path)
        LOGGER.info("Wrote %s", events_path)
        LOGGER.info("Wrote %s", summary_path)
        LOGGER.info("Finished UCI Sprint 1 pipeline")
        return summary

    def normalize(self, max_cycles: int | None = None) -> pd.DataFrame:
        frames: list[pd.DataFrame] = []
        expected_cycles: int | None = None

        for spec in UCI_SENSOR_SPECS:
            path = self.raw_dir / spec.filename
            sensor_df = self._read_sensor_matrix(path, max_cycles=max_cycles)
            LOGGER.info(
                "Loaded %s with shape rows=%s cols=%s",
                spec.sensor_id,
                sensor_df.shape[0],
                sensor_df.shape[1],
            )

            if expected_cycles is None:
                expected_cycles = sensor_df.shape[0]
            elif sensor_df.shape[0] != expected_cycles:
                LOGGER.warning(
                    "Sensor %s has %s cycles, expected %s",
                    spec.sensor_id,
                    sensor_df.shape[0],
                    expected_cycles,
                )

            features = self._sensor_features(sensor_df, spec)
            frames.append(features)

        if not frames:
            raise ValueError("No sensor data found")

        normalized = frames[0]
        for frame in frames[1:]:
            normalized = normalized.merge(frame, on="cycle_id", how="outer")

        normalized.insert(1, "device_id", "UCI_HYDRAULIC_RIG_001")
        normalized.insert(2, "source_format", "uci_hydraulic_cycle_matrix")
        normalized.insert(3, "plant", "UCI_TEST_RIG")
        normalized.insert(4, "line", "HYDRAULIC_TEST_BENCH")
        normalized.insert(5, "source_timestamp", normalized["cycle_id"].map(self._cycle_timestamp))
        normalized.insert(6, "processed_at", normalized["source_timestamp"].map(self._processed_timestamp))
        return normalized

    def validate_quality(self, df: pd.DataFrame) -> pd.DataFrame:
        quality_status: list[str] = []
        quality_reason: list[str] = []

        for _, row in df.iterrows():
            missing_required = [
                field
                for field in ("cycle_id", "device_id", "source_timestamp")
                if pd.isna(row.get(field))
            ]
            if missing_required:
                quality_status.append("rejected")
                quality_reason.append("missing_" + ",".join(missing_required))
                continue

            ttl_status = self.check_ttl(row["source_timestamp"], row["processed_at"])
            if ttl_status != "valid":
                quality_status.append("historical_only")
                quality_reason.append("ttl_expired")
                continue

            sample_mismatches = self._sample_mismatch_reasons(row)
            if sample_mismatches:
                quality_status.append("quarantine")
                quality_reason.append(";".join(sample_mismatches))
                continue

            quality_status.append("valid")
            quality_reason.append("")

        result = df.copy()
        result["quality_status"] = quality_status
        result["quality_reason"] = quality_reason
        return result

    def check_ttl(self, source_timestamp: str, processed_at: str) -> str:
        source_dt = datetime.fromisoformat(source_timestamp.replace("Z", "+00:00"))
        processed_dt = datetime.fromisoformat(processed_at.replace("Z", "+00:00"))
        age = (processed_dt - source_dt).total_seconds()
        return "valid" if age <= self.ttl_seconds else "historical_only"

    def generate_candidate_events(self, df: pd.DataFrame) -> list[dict[str, Any]]:
        events: list[dict[str, Any]] = []
        valid_df = df[df["quality_status"] == "valid"]

        for _, row in valid_df.iterrows():
            conditions = self._degraded_conditions(row)
            if not conditions:
                continue
            events.append(
                {
                    "event_type": "maintenance_alert_candidate",
                    "device_id": row["device_id"],
                    "cycle_id": int(row["cycle_id"]),
                    "plant": row["plant"],
                    "source_timestamp": row["source_timestamp"],
                    "processed_at": row["processed_at"],
                    "severity": self._severity(conditions),
                    "conditions": conditions,
                    "recommended_action": "manual_review_before_sap_pm",
                    "quality_status": row["quality_status"],
                }
            )
        return events

    def build_summary(self, df: pd.DataFrame, events: list[dict[str, Any]]) -> dict[str, Any]:
        status_counts = df["quality_status"].value_counts().to_dict()
        return {
            "dataset": "uci_hydraulic",
            "cycles_processed": int(len(df)),
            "sensors_processed": len(UCI_SENSOR_SPECS),
            "quality_status_counts": {str(k): int(v) for k, v in status_counts.items()},
            "candidate_events": len(events),
            "sampling_integrity": [
                {
                    "sensor_id": spec.sensor_id,
                    "sampling_rate_hz": spec.sampling_rate_hz,
                    "expected_samples_per_cycle": spec.expected_samples,
                }
                for spec in UCI_SENSOR_SPECS
            ],
            "notes": [
                "Cycle-level normalization preserves original sampling rates.",
                "No upsampling or synthetic sensor readings are created.",
                "SAP events are candidates only; Sprint 1 does not integrate with SAP.",
            ],
        }

    def _load_profile(self, max_cycles: int | None = None) -> pd.DataFrame:
        path = self.raw_dir / "profile.txt"
        if not path.exists():
            raise FileNotFoundError(path)
        profile = pd.read_csv(path, sep="\t", header=None, nrows=max_cycles)
        profile.columns = [
            "cooler_condition_pct",
            "valve_condition_pct",
            "internal_pump_leakage",
            "hydraulic_accumulator_bar",
            "stable_flag",
        ]
        profile.insert(0, "cycle_id", range(1, len(profile) + 1))
        LOGGER.info("Loaded profile with %s cycles", len(profile))
        return profile

    def _read_sensor_matrix(self, path: Path, max_cycles: int | None = None) -> pd.DataFrame:
        if not path.exists():
            raise FileNotFoundError(path)
        return pd.read_csv(path, sep="\t", header=None, nrows=max_cycles)

    def _sensor_features(self, df: pd.DataFrame, spec: SensorSpec) -> pd.DataFrame:
        prefix = spec.sensor_id.lower()
        features = pd.DataFrame(
            {
                "cycle_id": range(1, len(df) + 1),
                f"{prefix}_sample_count": df.count(axis=1),
                f"{prefix}_expected_samples": spec.expected_samples,
                f"{prefix}_mean": df.mean(axis=1),
                f"{prefix}_min": df.min(axis=1),
                f"{prefix}_max": df.max(axis=1),
                f"{prefix}_std": df.std(axis=1),
                f"{prefix}_first": df.iloc[:, 0],
                f"{prefix}_last": df.iloc[:, -1],
            }
        )
        return features

    def _cycle_timestamp(self, cycle_id: int) -> str:
        timestamp = self.base_timestamp + timedelta(seconds=(int(cycle_id) - 1) * 60)
        return timestamp.isoformat().replace("+00:00", "Z")

    def _processed_timestamp(self, source_timestamp: str) -> str:
        source_dt = datetime.fromisoformat(source_timestamp.replace("Z", "+00:00"))
        return (source_dt + timedelta(seconds=1)).isoformat().replace("+00:00", "Z")

    def _sample_mismatch_reasons(self, row: pd.Series) -> list[str]:
        reasons: list[str] = []
        for spec in UCI_SENSOR_SPECS:
            prefix = spec.sensor_id.lower()
            observed = row.get(f"{prefix}_sample_count")
            if pd.isna(observed):
                reasons.append(f"{spec.sensor_id}:missing_sensor")
            elif int(observed) != spec.expected_samples:
                reasons.append(f"{spec.sensor_id}:sample_count_{int(observed)}_expected_{spec.expected_samples}")
        return reasons

    def _degraded_conditions(self, row: pd.Series) -> list[str]:
        conditions: list[str] = []
        if row["cooler_condition_pct"] < 100:
            conditions.append(f"cooler_condition_{int(row['cooler_condition_pct'])}pct")
        if row["valve_condition_pct"] < 100:
            conditions.append(f"valve_condition_{int(row['valve_condition_pct'])}pct")
        if row["internal_pump_leakage"] > 0:
            conditions.append(f"pump_leakage_level_{int(row['internal_pump_leakage'])}")
        if row["hydraulic_accumulator_bar"] < 130:
            conditions.append(f"accumulator_pressure_{int(row['hydraulic_accumulator_bar'])}bar")
        if row["stable_flag"] == 1:
            conditions.append("unstable_cycle")
        return conditions

    def _severity(self, conditions: list[str]) -> str:
        severe_tokens = ("3pct", "73pct", "level_2", "90bar")
        if any(token in condition for condition in conditions for token in severe_tokens):
            return "high"
        if len(conditions) >= 2:
            return "medium"
        return "low"


def configure_logging(level: str = "INFO") -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Daikibo Telemetry Sprint 1 pipeline")
    parser.add_argument("--raw-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--max-cycles", type=int, default=None)
    parser.add_argument("--log-level", default="INFO")
    args = parser.parse_args()

    configure_logging(args.log_level)
    processor = TelemetryProcessor(raw_dir=args.raw_dir, output_dir=args.output_dir)
    summary = processor.run_uci_sprint1(max_cycles=args.max_cycles)
    LOGGER.info("Summary: %s", json.dumps(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

