# Architecture

## Vision general

La solucion se disena como una arquitectura de dos capas:

1. Capa analitica para recibir, limpiar, normalizar y explotar telemetria.
2. Capa transaccional para enviar solo eventos procesados hacia SAP.

## Flujo conceptual

```text
IIoT Sensors
  -> Raw Telemetry Format A / Format B
  -> Python Normalization Pipeline
  -> Data Quality Classification
  -> Time-Windowing / TTL Validation
  -> MDM Asset Mapping
  -> Unified Telemetry Dataset
  -> Analytics / Availability / Anomaly Detection
  -> Optional SAP PP Join for Full OEE
  -> Processed Events
  -> SAP PM / SAP MM / SAP CO
```

## Capa analitica

Responsabilidades:

- Recibir datos crudos de telemetria.
- Homologar formatos fuente.
- Validar contratos de datos.
- Consolidar la vista unica de maquina, planta y timestamp.
- Calcular o preparar metricas operativas, empezando por disponibilidad.
- Cruzar la telemetria con SAP PP cuando se requiera OEE completo.
- Servir como base para reporteria y modelos predictivos.

Ejemplos de destino:

- Data Lake.
- Base analitica.
- Archivos particionados.
- Dataset para BI.

## Capa transaccional

Responsabilidades:

- Recibir solo eventos accionables.
- Disparar procesos ERP.
- Evitar sobrecargar SAP con registros crudos de alta frecuencia.
- Validar que el activo exista en SAP antes de intentar crear una orden.

Ejemplos de eventos:

```json
{
  "event_type": "maintenance_alert",
  "device_id": "MACHINE_004",
  "sap_equipment_number": "10004562",
  "sap_functional_location": "TOKYO-LINE-02-CUTTER-04",
  "plant": "Tokyo",
  "metric": "vibration",
  "severity": "high",
  "source_timestamp": "2026-05-22T14:03:10Z",
  "processed_at": "2026-05-22T14:03:11Z",
  "recommended_action": "create_preventive_maintenance_order"
}
```

## Integracion SAP

- SAP PM: creacion de orden de mantenimiento preventivo.
- SAP MM: verificacion de stock y solicitud de pedido de repuesto.
- SAP CO: analisis de impacto en costos, margen y desviaciones.
- SAP PP: fuente futura para completar OEE con rendimiento y calidad.

## Mapeo maestro de activos

SAP no necesariamente reconoce el identificador tecnico del sensor IIoT. Por eso, antes de enviar un evento a SAP, el pipeline debe resolver el mapeo:

```text
device_id -> SAP Equipment Number / Functional Location / Asset ID
```

Si no existe mapeo valido, el evento no debe disparar procesos transaccionales y debe quedar en una cola de revision.

## Manejo de datos atrasados

El pipeline debe comparar el timestamp de origen contra el tiempo de procesamiento. Si el evento supera el TTL definido, por ejemplo 5 minutos, puede almacenarse para analisis historico, pero no debe crear una alerta transaccional en SAP.

Esto evita que una falla de red genere ordenes de mantenimiento tardias o incorrectas.

## Calidad de datos

Antes de usar un registro para analisis o automatizacion, el pipeline debe clasificar su estado:

```text
valid -> puede usarse para analisis y eventos
historical_only -> puede usarse para analisis historico, no para SAP
quarantine -> requiere revision
rejected -> no puede usarse
```

Esta clasificacion evita decisiones automaticas basadas en telemetria incompleta, duplicada, corrupta, atrasada o sin mapeo maestro.

## Escalabilidad y costos

La arquitectura debe priorizar servicios PaaS o serverless, como AWS Lambda, colas administradas, Databricks Jobs o equivalentes, para escalar bajo demanda y pagar por ejecucion en lugar de mantener servidores ociosos.

## Riesgos mitigados

- Excel no escala para telemetria de alta frecuencia.
- SAP no debe funcionar como repositorio de datos crudos IIoT.
- Un modelo sin trazabilidad impide auditoria y mejora continua.
- Mezclar logica tecnica y narrativa ejecutiva dificulta mantenimiento.
- Eventos atrasados pueden generar acciones operativas incorrectas.
- Falta de mapeo maestro puede impedir la creacion de ordenes SAP.
