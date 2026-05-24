# Business Requirements

## Contexto

Daikibo opera maquinaria industrial en planta y recibe telemetria en mas de un formato. La falta de un modelo unificado impide comparar maquinas, calcular metricas operativas consistentes y convertir senales tecnicas en acciones de negocio.

## Alcance Supply Chain

El impacto del proyecto esta en Manufacturing / Shop Floor.

Fuera de alcance inicial:

- Inbound: abastecimiento de acero, piezas o materias primas.
- Outbound: entrega de maquinaria terminada al cliente.

Dentro de alcance:

- Unificacion de telemetria de maquinas.
- Estandarizacion de atributos operativos.
- Base para medicion del pilar Availability del OEE.
- Generacion futura de alertas para mantenimiento y materiales.
- Mapeo entre sensores IIoT y activos maestros de SAP.

## Objetivo de negocio

Como area de operaciones de Daikibo, necesitamos consolidar los formatos A y B de telemetria industrial para obtener una vista unica del estado de las maquinas, habilitar el pilar de disponibilidad del OEE y generar alertas procesables hacia SAP PM/MM sin saturar el ERP con datos crudos.

Para calcular OEE completo, la capa analitica debera cruzar esta telemetria con datos de produccion provenientes de SAP PP, incluyendo ordenes de fabricacion, unidades producidas y unidades defectuosas.

## Requerimientos funcionales

1. Ingerir datos de telemetria desde al menos dos formatos fuente.
2. Normalizar campos tecnicos hacia un contrato comun.
3. Preservar el origen del dato para trazabilidad.
4. Validar campos minimos: maquina, timestamp, metrica, valor y planta.
5. Generar una salida consolidada lista para analisis.
6. Separar datos crudos de eventos accionables.
7. Aplicar logica de ventanas de tiempo y TTL: no enviar alertas transaccionales a SAP cuando la diferencia entre el timestamp de origen y el tiempo de procesamiento supere 5 minutos.
8. Preparar una estructura futura para alertas de mantenimiento.
9. Cruzar el `device_id` del sensor con una tabla de mapeo MDM para obtener el Equipment Number o Functional Location reconocido por SAP.
10. Clasificar datos sucios antes de cualquier decision operativa.

## Calidad de datos

El pipeline no debe borrar ni corregir silenciosamente datos sucios. Cada registro debe quedar clasificado en una de estas categorias:

- `valid`: dato apto para analisis y, si aplica, generacion de eventos.
- `historical_only`: dato util para analisis historico, pero no apto para acciones transaccionales.
- `quarantine`: dato sospechoso que requiere revision antes de usarse.
- `rejected`: dato invalido que no puede usarse por falta de campos criticos o errores estructurales.

Reglas iniciales:

1. Si falta `device_id`, `source_timestamp`, `metric` o `value`, el registro debe marcarse como `rejected`.
2. Si el valor esta fuera de un rango fisico posible, el registro debe marcarse como `quarantine`.
3. Si el valor esta fuera del rango operativo esperado pero es fisicamente posible, el registro puede generar una anomalia.
4. Si el evento esta duplicado, debe conservarse un solo registro y registrar el descarte.
5. Si el evento supera el TTL definido, debe marcarse como `historical_only` y no generar alerta SAP.
6. Si el `device_id` no tiene mapeo valido contra activos SAP, puede conservarse para analisis, pero no debe generar evento transaccional.

## Requerimientos no funcionales

1. El diseno debe evitar dependencia de Excel como repositorio principal.
2. El pipeline debe poder escalar a altos volumenes de telemetria.
3. La integracion con SAP debe limitarse a eventos procesados.
4. El modelo debe ser auditable y reproducible.
5. La estructura del proyecto debe separar contratos, pipeline, muestras, outputs y narrativa ejecutiva.
6. El sistema debe validar que el `device_id` exista en el maestro de activos antes de ingerir o procesar eventos criticos.
7. La arquitectura de procesamiento debe priorizar servicios PaaS o serverless para escalar bajo demanda y reducir costos de infraestructura ociosa.

## KPIs

- OEE.
- Availability del OEE.
- Downtime no planificado.
- Tiempo de deteccion de anomalias.
- Tiempo de generacion de orden preventiva.
- Disponibilidad de repuestos criticos.
- Desviacion del costo estandar por unidad.
- Porcentaje de mensajes de telemetria procesados sin error.
- Latencia de ingesta menor a 2 segundos para eventos en linea.
- Porcentaje de eventos descartados por TTL vencido.

## Frase ejecutiva

Esta unificacion de datos constituye el paso cero para automatizar flujos en los modulos PM y MM del ERP, habilitando mantenimiento predictivo, compras Just-in-Time de repuestos y control financiero del impacto operativo en CO, sin confundir el ERP con un repositorio de telemetria cruda.
