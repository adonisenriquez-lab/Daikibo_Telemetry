# SAP Event Schema

## Proposito

Definir el contrato de salida para eventos procesados que si pueden enviarse a SAP.

Este contrato representa alertas ya filtradas, enriquecidas y validadas, no telemetria cruda.

## Campos minimos

| Campo | Descripcion | Ejemplo |
| --- | --- | --- |
| `event_type` | Tipo de evento procesado | `maintenance_alert` |
| `device_id` | Identificador de origen IIoT | `MACHINE_004` |
| `sap_equipment_number` | Equipo SAP PM resuelto por MDM | `10004562` |
| `sap_functional_location` | Ubicacion funcional SAP PM | `TOKYO-LINE-02-CUTTER-04` |
| `plant` | Planta industrial | `Tokyo` |
| `metric` | Metrica que disparo el evento | `vibration` |
| `severity` | Severidad normalizada | `high` |
| `source_timestamp` | Timestamp original del evento | `2026-05-22T14:03:10Z` |
| `processed_at` | Timestamp de procesamiento | `2026-05-22T14:03:11Z` |
| `recommended_action` | Accion sugerida para SAP | `create_preventive_maintenance_order` |

## Reglas funcionales

- No se debe generar evento SAP si el TTL esta vencido.
- No se debe generar evento SAP si no existe mapeo valido contra activos SAP.
- El evento debe contener una accion recomendada clara.
- SAP recibe eventos accionables, no series crudas de telemetria.
