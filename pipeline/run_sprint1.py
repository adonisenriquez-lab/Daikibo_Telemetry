from __future__ import annotations

from pathlib import Path

from telemetry_processor import TelemetryProcessor, configure_logging


def main() -> int:
    project_root = Path(__file__).resolve().parents[1]
    raw_dir = project_root / "input_samples" / "uci_hydraulic" / "raw"
    output_dir = project_root / "output" / "sprint1_uci"

    configure_logging("INFO")
    processor = TelemetryProcessor(raw_dir=raw_dir, output_dir=output_dir)
    processor.run_uci_sprint1()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

