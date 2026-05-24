# Daikibo Telemetry

Proyecto de diseno e implementacion para unificar telemetria industrial de Daikibo y convertir datos IIoT heterogeneos en informacion operativa util para manufactura, mantenimiento y control financiero. (EL CASO ES UNA SIMULACION DE BUSSINES REQUIREMENT)

## Objetivo

Unificar formatos de telemetria de maquinas industriales para obtener visibilidad completa del Shop Floor, habilitar el pilar de disponibilidad del OEE y preparar eventos procesados que puedan integrarse con SAP PM, MM y CO.

## Estructura

```text
Daikibo_Telemetry/
  data_contracts/       # Contratos de datos y esquemas funcionales
  input_samples/        # Archivos fuente de ejemplo por formato
    format_a/
    format_b/
  pipeline/             # Normalizacion, validacion y consolidacion
  output/               # Salidas generadas por el pipeline
  prompts_entregable/   # Narrativa ejecutiva y textos del caso
  tests/                # Pruebas de validacion del modelo y pipeline
```

## Principios de diseno

La telemetria cruda no debe enviarse directamente a SAP ni limitarse a Excel. El pipeline actua como middleware analitico: limpia, normaliza y consolida los datos; luego solo envia eventos procesados y accionables hacia sistemas transaccionales.

El calculo completo de OEE requiere cruzar esta telemetria con datos de produccion de SAP PP, porque rendimiento y calidad dependen de ordenes de fabricacion, unidades producidas y unidades rechazadas.

Antes de enviar una alerta a SAP, el pipeline debe traducir el `device_id` del sensor al activo reconocido por SAP, como Equipment Number o Functional Location.

## Valor de negocio

- OEE: base confiable para disponibilidad; integracion futura con SAP PP para rendimiento y calidad.
- SAP PM: mantenimiento preventivo basado en anomalias.
- SAP MM: validacion y solicitud de repuestos Just-in-Time.
- SAP CO: proteccion del costo estandar y margen operativo.

## Documentos de decision

- `business_requirements.md`: alcance funcional y reglas de negocio.
- `architecture.md`: arquitectura analitica/transaccional.
- `business_case_simulation.md`: ROI ilustrativo y supuestos.
- `pilot_validation_plan.md`: plan de validacion por sprints.
- `risk_mitigation.md`: riesgos y mitigaciones antes de escalar.
- `executive_one_pager.md`: resumen ejecutivo para comite.

## Sprint 1 v0.0001

Ejecutar pipeline UCI completo:

```text
python pipeline/run_sprint1.py
```

Salidas:

```text
output/sprint1_uci/
  uci_cycle_features.csv
  sap_candidate_events.json
  quality_report.json
```

La normalizacion es por ciclo de 60 segundos. El pipeline respeta las frecuencias originales de cada sensor y no inventa lecturas mediante upsampling.
