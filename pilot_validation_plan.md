# Pilot Validation Plan

## Proposito

Definir un piloto gradual para evitar invertir en una integracion completa antes de validar datos, alertas y adopcion operativa.

## Sprint 1: Prueba tecnica con UCI Hydraulic

Duracion estimada: 2 semanas.

Objetivo:

Validar que el pipeline puede leer, normalizar, clasificar y producir eventos candidatos usando un dataset industrial publico.

Entregables:

- Normalizacion de sensores UCI hacia el contrato unificado.
- Clasificacion de calidad: `valid`, `historical_only`, `quarantine`, `rejected`.
- Resumen de ciclos procesados.
- Eventos candidatos de condicion/falla.

Criterios de exito:

- Procesar los 2,205 ciclos sin error estructural.
- Clasificar mas del 95% de registros.
- Generar metricas del pipeline.
- Producir salida auditable en `output/`.
- Ejecutar stress test duplicando sinteticamente el dataset hasta 10,000 ciclos.
- Mantener latencia de procesamiento menor a 2 segundos por ciclo en ambiente piloto.

Criterios de falla:

- Mas de 10% de registros validos clasificados como `rejected`.
- Pipeline no reproducible.
- Salidas sin trazabilidad hacia sensor/ciclo.

## Sprint 2: Validacion con 1 maquina Daikibo real

Duracion estimada: 2 semanas.

Objetivo:

Validar si los datos reales de una maquina critica pueden entrar al modelo sin redisenar todo el pipeline.

Entregables:

- Muestra de telemetria real de una maquina.
- Mapeo inicial `device_id -> activo SAP`.
- Reporte de calidad de datos reales.
- Comparacion entre dataset UCI y datos Daikibo.

Criterios de exito:

- Mas del 90% de eventos reales clasificados.
- Mapeo maestro disponible para la maquina piloto.
- Identificacion clara de brechas de formato.

Criterios de falla:

- Formato real incompatible sin refactor mayor.
- Falta de acceso a datos de maquina.
- No existe responsable para mapeo maestro.

## Sprint 3: Validacion operativa de alertas

Duracion estimada: 2 semanas.

Objetivo:

Validar si las alertas son utiles para mantenimiento antes de automatizar SAP PM.

Entregables:

- Alertas generadas en modo manual.
- Revision diaria por un tecnico de mantenimiento.
- Registro de falsos positivos, falsos negativos y acciones tomadas.
- Recomendacion GO/NO-GO.

Criterios de exito:

- Tecnicos consideran utiles las alertas.
- Falsos positivos bajo umbral aceptado.
- Al menos una anomalia util detectada o una regla validada por experto.
- Tiempo de revision operativo aceptable.

Criterios de falla:

- Falsos positivos mayores a 40%.
- Tecnicos ignoran o descartan sistematicamente las alertas.
- Alertas no accionables.
- No se puede conectar alerta con proceso de mantenimiento.

## Calibracion de umbrales

Durante Sprint 3, las reglas de alerta deben ajustarse con feedback del tecnico de mantenimiento:

1. Semana 1: usar umbrales conservadores para no perder senales relevantes.
2. Revision diaria: clasificar cada alerta como util, falso positivo o no accionable.
3. Ajuste: recalibrar umbrales con base en la revision.
4. Semana 2: validar si la tasa de falsos positivos baja hacia un objetivo menor a 20%.

La meta del piloto no es tener el modelo perfecto, sino demostrar que las alertas pueden converger hacia utilidad operativa.

## Quick wins esperados

| Momento | Quick win | Audiencia |
| --- | --- | --- |
| Semana 2 | Pipeline procesa UCI y genera metricas reproducibles | CTO / TI |
| Semana 4 | Primera visualizacion de datos reales Daikibo normalizados | Planta / Operaciones |
| Semana 6 | Primera alerta util revisada por tecnico | CFO / COO |

Cada quick win justifica continuar al siguiente sprint sin comprometer inversion enterprise.

## Presupuesto estimado

| Sprint | Recurso | Costo estimado |
| --- | --- | --- |
| Sprint 1 | Desarrollador Python, 2 semanas al 50% | USD 4,000 |
| Sprint 1 | Infraestructura dev local/cloud minima | USD 200 |
| Sprint 2 | Desarrollador Python, 2 semanas al 75% | USD 6,000 |
| Sprint 2 | Acceso a maquina Daikibo y sensores | USD 2,000 |
| Sprint 2 | Tiempo equipo OT/mantenimiento | USD 3,000 |
| Sprint 3 | Desarrollador Python, 2 semanas al 50% | USD 4,000 |
| Sprint 3 | Tecnico de mantenimiento dedicado | USD 5,000 |
| Sprint 3 | Consultor SAP para evaluacion de integracion | USD 5,000 |
| Total base |  | USD 29,200 |
| Contingencia 20% |  | USD 5,840 |
| Total piloto |  | USD 35,040 |

La inversion piloto se redondea a USD 35,000. Si falla Sprint 3, el costo perdido es menor que avanzar prematuramente a una inversion enterprise de USD 250,000.

## RACI Matrix

| Actividad | Responsable | Aprueba | Consulta | Informa |
| --- | --- | --- | --- | --- |
| Sprint 1 ejecucion tecnica | Dev Python | CTO | Data/BI | CFO |
| Sprint 2 acceso a maquina | Jefe de Planta | COO | OT Manager | CTO |
| Sprint 2 mapeo maestro | Data Owner MDM | CTO | Jefe Mantenimiento | COO |
| Sprint 3 validacion de alertas | Tecnico de Mantenimiento | Jefe Mantenimiento | Dev Python | CFO |
| Evaluacion SAP PM | Consultor SAP | CTO | BASIS/ABAP | CFO |
| Decision GO/NO-GO | CFO | CEO | CTO, COO | Comite |

## Decision GO/NO-GO

Avanzar a integracion SAP y escalamiento solo si:

- Sprint 1 demuestra viabilidad tecnica.
- Sprint 2 demuestra compatibilidad con datos reales.
- Sprint 3 demuestra utilidad operativa.

Si falla Sprint 2 o Sprint 3, detener el programa y documentar aprendizajes antes de solicitar inversion mayor.
