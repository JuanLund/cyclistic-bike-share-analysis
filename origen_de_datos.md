# Origen y Estructura de los Datos (Data Source)

## Fuente Oficial y Licencia
Los datos utilizados en este caso de estudio corresponden a registros históricos de viajes de los últimos 12 meses del programa de bicicletas compartidas Cyclistic (basados en datos reales del sistema Divvy de Chicago). 

Los conjuntos de datos son de acceso público y han sido proporcionados directamente por **Motivate International Inc.** bajo una [licencia pública de uso de datos](https://divvybikes.com/data-license-agreement).

* **Enlace de descarga de datos crudos:** [Repositorio AWS - Divvy Tripdata](https://divvy-tripdata.s3.amazonaws.com/index.html)

## Volumen y Almacenamiento
* **Período de análisis:** Últimos 12 meses.
* **Volumen inicial (crudo):** 12 archivos CSV mensuales individuales que totalizan **6,171,785 filas**.
* **Consolidación de Arquitectura:** Para optimizar la velocidad de lectura, escritura y el procesamiento en memoria a través de Python (Pandas), los 12 archivos fueron unificados, limpiados y exportados como un único archivo columnar comprimido en formato **`.parquet`** (`cyclistic_12_meses.parquet`). Tras la limpieza, la base auditada final cuenta con **4,810,648 filas válidas**.

## Restricciones de Privacidad de Datos (Ausencia de PII)
En estricto cumplimiento con las regulaciones de privacidad y protección de datos comerciales, este conjunto de datos excluye de manera deliberada toda Información de Identificación Personal (PII, por sus siglas en inglés).

* **Limitación:** El dataset no contiene columnas de `user_id`, nombres, direcciones, ni números de tarjetas de crédito o facturación.
* **Implicación analítica:** Dado que no es posible rastrear mediante un ID primario cuántas veces un mismo usuario casual compra pases individuales, el análisis requirió el diseño de **proxies comportamentales**. Se utilizaron cruces de variables espaciales y temporales (día de la semana, tipo de bicicleta, duración y ubicación de estaciones residenciales vs. turísticas) para estimar patrones de recurrencia e identificar a la población residente convertible.

## Diccionario de Datos (Esquema del Proyecto)
A continuación se detallan las variables clave utilizadas en el modelo descriptivo final:

### Variables Originales Conservadas
* `ride_id`: Identificador único alfanumérico generado para cada viaje individual.
* `rideable_type`: Tipo de bicicleta utilizada por el usuario (`classic_bike`, `electric_bike`, o bicicletas asistidas catalogadas inicialmente como `docked_bike`).
* `started_at`: Marca temporal exacta del inicio del viaje (formato `YYYY-MM-DD HH:MM:SS`).
* `ended_at`: Marca temporal exacta de la finalización del viaje.
* `start_station_name` / `end_station_name`: Nombres oficiales de las estaciones físicas de origen y destino en Chicago.
* `member_casual`: Tipología transaccional del cliente. Valores posibles: `member` (usuario con suscripción anual activa) o `casual` (usuario que adquirió un pase de viaje único o de día completo).

### Variables Generadas (Ingeniería de Características)
Durante la fase de procesamiento en Python, se agregaron las siguientes columnas esenciales para el análisis bimodal:
* `ride_length`: Duración exacta del trayecto expresada en minutos (resultado de `ended_at` - `started_at`). Variable clave para determinar la fricción económica y el sobrecosto del usuario ocasional.
* `day_of_week`: Valor extraído de `started_at` para identificar el día de inicio del viaje (del 1 al 7), posteriormente mapeado a texto (Lunes a Domingo) para su ingesta directa y visualización en Tableau.