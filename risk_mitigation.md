# Risk Mitigation

## Proposito

Identificar riesgos principales del piloto Daikibo Telemetry y definir mitigaciones antes de invertir en automatizacion completa.

## Riesgos principales

| Riesgo | Probabilidad | Impacto | Mitigacion |
| --- | --- | --- | --- |
| UCI no representa las maquinas Daikibo | Media | Alto | Usar UCI solo en Sprint 1 y validar con maquina real en Sprint 2 |
| Falsos positivos generan fatiga de alertas | Alta | Critico | Medir falsos positivos en Sprint 3 antes de automatizar SAP |
| SAP PM no responde en tiempo util | Media | Alto | Mantener Sprint 3 en modo manual y evaluar tiempos reales antes de integracion |
| Mapeo MDM obsoleto | Alta | Alto | Definir responsable de datos maestros y regla de bloqueo si no hay mapeo valido |
| Nuevos formatos rompen pipeline | Media | Medio | Disenar normalizadores por fuente y contrato unificado estable |
| Datos atrasados disparan acciones incorrectas | Media | Alto | Aplicar TTL y clasificar eventos vencidos como `historical_only` |
| Tecnicos no confian en alertas | Alta | Critico | Incluir usuario de mantenimiento en Sprint 3 y medir aceptacion |
| Costos cloud crecen sin control | Media | Medio | Mantener piloto local o acotado; pasar a PaaS/serverless solo tras GO |

## Principios de control

- No automatizar SAP antes de validar alertas manuales.
- No pedir inversion enterprise con solo dataset publico.
- No usar eventos sin mapeo maestro para acciones transaccionales.
- No borrar datos sucios silenciosamente.
- No prometer OEE completo sin integrar SAP PP.

## Plan B

Si el piloto no demuestra valor operativo:

1. Mantener solo el pipeline como herramienta analitica.
2. Usarlo para reporting historico y aprendizaje de datos.
3. No avanzar a integracion SAP automatica.
4. Documentar brechas de datos reales para una futura fase.

## Decision recomendada

La estrategia correcta no es aprobar USD 250K desde el inicio. La estrategia correcta es invertir poco, aprender rapido y escalar solo despues de evidencia operativa.

