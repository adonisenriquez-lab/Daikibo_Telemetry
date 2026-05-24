# Daikibo Telemetry: Piloto de Validacion

## Problema

El downtime no planificado puede convertir fallos tecnicos en impacto financiero directo: reparaciones correctivas, perdida de produccion, urgencias de repuestos y desviaciones de costo.

## Solucion propuesta

Validar un pipeline que normaliza telemetria IIoT, clasifica calidad de datos y genera alertas candidatas para mantenimiento preventivo.

```text
Sensores -> Pipeline -> Alertas utiles -> Mantenimiento preventivo
```

## ROI proyectado

Supuesto ilustrativo:

- 50 maquinas criticas.
- 1 fallo critico por maquina por ano.
- Costo correctivo por fallo: USD 50,000.
- Costo preventivo por intervencion: USD 15,000.
- 70% de fallos convertibles a preventivos.

Resultado simulado:

- Ahorro anual potencial: USD 1,225,000.
- Inversion para escalar: USD 250,000.
- ROI ilustrativo: 4.9x.
- Payback ilustrativo: 2.4 meses.

## Piloto propuesto

Duracion: 6 semanas.

Presupuesto: USD 35,000.

| Sprint | Objetivo | Costo |
| --- | --- | --- |
| Sprint 1 | Validar pipeline con UCI Hydraulic | USD 4,200 |
| Sprint 2 | Validar datos reales de 1 maquina Daikibo | USD 11,000 |
| Sprint 3 | Validar alertas con tecnico de mantenimiento | USD 14,000 |
| Contingencia | 20% | USD 5,840 |

## Decision GO/NO-GO

Avanzar a inversion enterprise solo si:

- el pipeline funciona tecnicamente;
- los datos reales son compatibles;
- las alertas son utiles para mantenimiento;
- el baseline operativo confirma oportunidad de ahorro.

## Pregunta al comite

Se solicita aprobar USD 35,000 para validar en 6 semanas si existe una oportunidad de ahorro anual potencial de USD 1.2M antes de considerar una inversion enterprise de USD 250,000.

