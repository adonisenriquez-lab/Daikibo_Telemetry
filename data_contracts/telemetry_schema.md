# Unified Telemetry Schema

## Proposito

Definir el contrato comun para datos de telemetria normalizados desde multiples formatos fuente.

## Campos minimos

| Campo | Descripcion | Ejemplo |
| --- | --- | --- |
| `device_id` | Identificador del sensor o maquina en la capa IIoT | `MACHINE_004` |
| `source_format` | Formato de origen | `format_a` |
| `plant` | Planta industrial | `Tokyo` |
| `line` | Linea o area productiva | `Line 02` |
| `source_timestamp` | Timestamp generado por la maquina o sensor | `2026-05-22T14:03:10Z` |
| `processed_at` | Timestamp de procesamiento por el pipeline | `2026-05-22T14:03:11Z` |
| `metric` | Metrica reportada | `vibration` |
| `value` | Valor numerico o categorico | `0.82` |
| `unit` | Unidad de medida | `mm/s` |
| `status` | Estado operacional si existe | `running` |
| `quality_status` | Estado de calidad del dato | `valid` |
| `quality_reason` | Motivo de clasificacion, si aplica | `ttl_expired` |

## Reglas funcionales

- `device_id`, `source_timestamp`, `processed_at`, `metric` y `value` son obligatorios.
- Los eventos deben conservar `source_format` para trazabilidad.
- La diferencia entre `processed_at` y `source_timestamp` define la edad del evento.
- Los eventos mayores al TTL definido pueden almacenarse para analisis historico, pero no deben disparar acciones transaccionales en SAP.
- Todo evento debe tener un `quality_status`: `valid`, `historical_only`, `quarantine` o `rejected`.
