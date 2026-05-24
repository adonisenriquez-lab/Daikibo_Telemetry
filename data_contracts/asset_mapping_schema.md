# Asset Mapping Schema

## Proposito

Traducir identificadores de sensores IIoT al maestro de activos reconocido por SAP.

El pipeline no debe enviar eventos transaccionales a SAP usando unicamente `device_id`, porque SAP PM y FI-AA trabajan con identificadores maestros como Equipment Number, Functional Location o Asset ID.

## Campos minimos

| Campo | Descripcion | Ejemplo |
| --- | --- | --- |
| `device_id` | Identificador tecnico del sensor o maquina en la capa IIoT | `MACHINE_004` |
| `sap_equipment_number` | Numero de equipo en SAP PM | `10004562` |
| `sap_functional_location` | Ubicacion funcional en SAP PM | `TOKYO-LINE-02-CUTTER-04` |
| `sap_asset_id` | Identificador de activo fijo en SAP FI-AA, si aplica | `AA-90004562` |
| `plant` | Planta o fabrica | `Tokyo` |
| `line` | Linea productiva | `Line 02` |
| `is_active` | Indica si el mapeo esta vigente | `true` |
| `valid_from` | Fecha inicial de vigencia | `2026-01-01` |
| `valid_to` | Fecha final de vigencia, si aplica | `null` |

## Regla funcional

Si un evento no puede resolverse contra esta tabla, debe quedar excluido de la integracion transaccional con SAP y enviarse a revision de datos maestros.
