# Business Case Simulation

## Proposito

Este documento no afirma ROI real de Daikibo. Define una simulacion conservadora para decidir si vale la pena avanzar desde una prueba tecnica hacia un piloto con maquina real.

## Separacion de objetivos

```text
Sprint 1: Validar pipeline tecnico con UCI Hydraulic
Sprint 2: Validar datos reales con 1 maquina Daikibo
Sprint 3: Validar utilidad operativa con tecnicos
```

El dataset UCI sirve para probar la capa analitica. No basta para aprobar una inversion enterprise.

## Baseline simulado

Supuestos para discusion ejecutiva:

| Variable | Supuesto conservador |
| --- | --- |
| Maquinas criticas en alcance futuro | 50 |
| Fallos criticos por maquina por ano | 1 |
| Costo correctivo por fallo | USD 50,000 |
| Costo preventivo por intervencion | USD 15,000 |
| Fallos convertibles a preventivos | 70% |
| Inversion estimada para escalar | USD 250,000 |

## Calculo ilustrativo

```text
Ahorro por fallo convertido = 50,000 - 15,000 = USD 35,000
Fallos convertidos por ano = 50 maquinas * 70% = 35
Ahorro anual estimado = 35 * 35,000 = USD 1,225,000
ROI ilustrativo = 1,225,000 / 250,000 = 4.9x
Payback ilustrativo = 250,000 / 1,225,000 * 12 = 2.4 meses
```

## Analisis de sensibilidad

| Escenario | Fallos por maquina/ano | Fallos totales/ano | % convertible | Ahorro anual | ROI sobre USD 250,000 |
| --- | --- | --- | --- | --- | --- |
| Optimista | 1.0 | 50 | 70% | USD 1,225,000 | 4.9x |
| Base | 0.7 | 35 | 50% | USD 612,500 | 2.5x |
| Pesimista | 0.5 | 25 | 30% | USD 262,500 | 1.1x |

Incluso en el escenario pesimista, la simulacion mantiene un ROI positivo. Aun asi, esta tabla no reemplaza la validacion con datos reales.

## Baseline operativo requerido

Antes de declarar mejora real, el piloto debe levantar el estado actual:

- Horas de downtime no planificado en el ultimo ano.
- Costo promedio por hora de downtime.
- Fallos correctivos por maquina critica.
- Tiempo promedio entre falla y orden de mantenimiento.
- Horas semanales dedicadas a revisar logs o reportes manuales.
- Porcentaje de mantenimiento preventivo vs correctivo.

## Lectura correcta

Esta simulacion solo muestra el tamano potencial del beneficio si las premisas se validan. La decision real de inversion debe depender del piloto con datos Daikibo reales.

## Metricas que deben validarse antes de escalar

- Costo real por hora de downtime.
- Horas reales de downtime evitable.
- Tasa real de falsos positivos.
- Tiempo real entre alerta y accion de mantenimiento.
- Porcentaje de eventos con mapeo SAP valido.
- Aceptacion del flujo por tecnicos de mantenimiento.

## Regla GO/NO-GO

No solicitar inversion enterprise hasta completar Sprint 3 y demostrar que las alertas generan valor operativo real.
