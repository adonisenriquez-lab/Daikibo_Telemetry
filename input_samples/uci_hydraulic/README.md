# UCI Hydraulic Condition Monitoring Dataset

## Fuente

Dataset publico: Condition Monitoring of Hydraulic Systems, UCI Machine Learning Repository.

Referencia:

Helwig, N., Pignanelli, E., & Schutze, A. (2015). Condition monitoring of hydraulic systems. UCI Machine Learning Repository. DOI: 10.24432/C5CW21.

Licencia: Creative Commons Attribution 4.0 International (CC BY 4.0).

## Uso en este proyecto

Este dataset se usa como muestra publica confiable para simular la capa analitica de Daikibo Telemetry:

```text
sensores industriales -> normalizacion -> calidad de datos -> deteccion de condicion -> evento candidato SAP PM
```

No representa datos reales de Daikibo ni una integracion real con SAP. Sirve para probar el pipeline, los contratos de datos y la narrativa de mantenimiento predictivo.

## Estructura local

```text
uci_hydraulic/
  README.md
  raw/
    description.txt
    documentation.txt
    profile.txt
    PS1.txt ... PS6.txt
    EPS1.txt
    FS1.txt FS2.txt
    TS1.txt ... TS4.txt
    VS1.txt
    CE.txt CP.txt SE.txt
```

La carpeta `raw/` debe tratarse como fuente intocable. Los archivos normalizados o derivados deben generarse fuera de `raw/`, por ejemplo en `output/`.

## Formato

- Cada fila representa un ciclo de operacion de 60 segundos.
- Cada archivo de sensor contiene una matriz tabulada.
- Las columnas representan mediciones dentro del ciclo.
- `profile.txt` contiene las condiciones objetivo por ciclo.

## Sensores

| Sensor | Cantidad fisica | Unidad | Frecuencia |
| --- | --- | --- | --- |
| PS1-PS6 | Presion | bar | 100 Hz |
| EPS1 | Potencia del motor | W | 100 Hz |
| FS1-FS2 | Flujo volumetrico | l/min | 10 Hz |
| TS1-TS4 | Temperatura | C | 1 Hz |
| VS1 | Vibracion | mm/s | 1 Hz |
| CE | Eficiencia de enfriamiento | % | 1 Hz |
| CP | Potencia de enfriamiento | kW | 1 Hz |
| SE | Factor de eficiencia | % | 1 Hz |

## Etiquetas en profile.txt

Cada fila de `profile.txt` corresponde al mismo ciclo de los archivos de sensores.

Columnas:

1. Cooler condition (%)
2. Valve condition (%)
3. Internal pump leakage
4. Hydraulic accumulator pressure (bar)
5. Stable flag

## Alcance del piloto

Este dataset permite medir:

- ciclos procesados;
- sensores normalizados;
- eventos validos, en cuarentena o rechazados;
- condiciones de falla por componente;
- eventos candidatos para mantenimiento preventivo.

No permite afirmar por si solo:

- OEE completo;
- reduccion real de downtime en Daikibo;
- ROI real;
- integracion SAP PM productiva.

