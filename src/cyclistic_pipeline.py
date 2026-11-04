#!/usr/bin/env python
# -*- coding: utf-8 -*-



# ======================================================================!pip install pyarrow

import os
print(os.getcwd())

import pandas as pd
import requests
import zipfile
import io
import os

# Lista de los últimos 12 meses
meses = [
    "202510", "202511", "202512",
    "202601", "202602", "202603", "202604", "202605", "202606", "202607", "202608", "202609"
]

base_url = "https://divvy-tripdata.s3.amazonaws.com/"
lista_df = []

for mes in meses:
    url = f"{base_url}{mes}-divvy-tripdata.zip"
    print(f"Descargando y procesando {mes}...")
    
    respuesta = requests.get(url)
    with zipfile.ZipFile(io.BytesIO(respuesta.content)) as z:
        csv_filename = [f for f in z.namelist() if f.endswith('.csv') and not f.startswith('__MACOSX')][0]
        with z.open(csv_filename) as f:
            df_mes = pd.read_csv(f)
            lista_df.append(df_mes)

print("Uniendo todos los datos...")
df_anual = pd.concat(lista_df, ignore_index=True)

# ---> AQUÍ GUARDAMOS DIRECTO EN EL DISCO D <---
# Cambia esta ruta si tu carpeta se llama distinto
ruta_destino = r"D:\Phyton_Analist\Proyect_cyclist\cyclistic_12_meses.parquet"

df_anual.to_parquet(ruta_destino, index=False)
print(f"¡Listo! Archivo guardado en: {ruta_destino}")

import pandas as pd
import numpy as np

# 1. Cargar los datos desde el archivo Parquet que creamos anteriormente
# Asegúrate de que el nombre del archivo coincida con el que guardaste
df = pd.read_parquet("cyclistic_12_meses.parquet")

print("Datos cargados. Filas iniciales:", len(df))

import pandas as pd
import numpy as np

# Usa la ruta completa donde guardamos el archivo
ruta_archivo = r"D:\Phyton_Analist\Proyect_cyclist\cyclistic_12_meses.parquet"
df = pd.read_parquet(ruta_archivo)

print("Datos cargados. Filas iniciales:", len(df))

# 2. Convertir las columnas de fecha a formato datetime
# Esto es necesario para poder realizar cálculos matemáticos con el tiempo
df['started_at'] = pd.to_datetime(df['started_at'])
df['ended_at'] = pd.to_datetime(df['ended_at'])

# 3. Crear la columna ride_length (Duración del viaje)
# Calculamos la diferencia y la convertimos a minutos para que sea más fácil de analizar
df['ride_length'] = (df['ended_at'] - df['started_at']).dt.total_seconds() / 60

# 4. Crear la columna day_of_week (Día de la semana)
# En Pandas, dayofweek da: 0=Lunes, 6=Domingo.
# El proyecto pide: 1=Domingo, 7=Sábado.
# Hacemos una fórmula matemática para hacer coincidir los formatos:
df['day_of_week'] = (df['started_at'].dt.dayofweek + 2) % 7
df['day_of_week'] = df['day_of_week'].replace(0, 7)

# 5. Revisar las primeras filas para confirmar los cambios
print("\nMuestra de las nuevas columnas:")
print(df[['started_at', 'ended_at', 'ride_length', 'day_of_week', 'member_casual']].head())

# 1. Eliminar filas con valores nulos (estaciones vacías, etc.)
df_limpio = df.dropna()

# 2. Filtrar viajes con duración negativa, cero o menores a 1 minuto
# Los viajes menores a 60 segundos suelen ser falsos arranques o usuarios que se arrepintieron
df_limpio = df_limpio[df_limpio['ride_length'] >= 1]

# 3. Filtrar viajes de mantenimiento
# A veces la empresa hace viajes de prueba y la estación se llama "HQ QR" o contiene "Test"
df_limpio = df_limpio[~df_limpio['start_station_name'].str.contains('Test|HQ QR', na=False, case=False)]

# Imprimir el resumen de la limpieza
filas_iniciales = len(df)
filas_finales = len(df_limpio)
filas_eliminadas = filas_iniciales - filas_finales

print(f"Filas iniciales: {filas_iniciales:,}")
print(f"Filas después de limpiar: {filas_finales:,}")
print(f"Se eliminaron {filas_eliminadas:,} filas con errores o incompletas.")

Python
# 1. Análisis descriptivo general
print("--- ESTADÍSTICAS GENERALES ---")
print(f"Duración promedio total: {df_limpio['ride_length'].mean():.2f} minutos")
print(f"Duración máxima total: {df_limpio['ride_length'].max():.2f} minutos")
print(f"Día más frecuente (Moda): {df_limpio['day_of_week'].mode()[0]}")

# 2. Análisis por tipo de usuario (member vs casual)
print("\n--- ANÁLISIS POR TIPO DE USUARIO ---")
# Promedio de duración
promedio_por_usuario = df_limpio.groupby('member_casual')['ride_length'].mean()
print("\nPromedio de duración (minutos):")
print(promedio_por_usuario)

# 3. Análisis cruzado: Tipo de usuario y día de la semana
# Promedio de duración por día (1=Dom, 7=Sáb)
promedio_dia_usuario = df_limpio.groupby(['day_of_week', 'member_casual'])['ride_length'].mean().unstack()
print("\nPromedio de duración por día de la semana:")
print(promedio_dia_usuario)

# Cantidad de viajes por día (1=Dom, 7=Sáb)
viajes_dia_usuario = df_limpio.groupby(['day_of_week', 'member_casual'])['ride_id'].count().unstack()
print("\nCantidad de viajes por día de la semana:")
print(viajes_dia_usuario)

print("--- ESTADÍSTICAS GENERALES ---")
print(f"Duración promedio total: {df_limpio['ride_length'].mean():.2f} minutos")
print(f"Duración máxima total: {df_limpio['ride_length'].max():.2f} minutos")
print(f"Día más frecuente (Moda): {df_limpio['day_of_week'].mode()[0]}")

# 2. Análisis por tipo de usuario (member vs casual)
print("\n--- ANÁLISIS POR TIPO DE USUARIO ---")
# Promedio de duración
promedio_por_usuario = df_limpio.groupby('member_casual')['ride_length'].mean()
print("\nPromedio de duración (minutos):")
print(promedio_por_usuario)

# 3. Análisis cruzado: Tipo de usuario y día de la semana
# Promedio de duración por día (1=Dom, 7=Sáb)
promedio_dia_usuario = df_limpio.groupby(['day_of_week', 'member_casual'])['ride_length'].mean().unstack()
print("\nPromedio de duración por día de la semana:")
print(promedio_dia_usuario)

# Cantidad de viajes por día (1=Dom, 7=Sáb)
viajes_dia_usuario = df_limpio.groupby(['day_of_week', 'member_casual'])['ride_id'].count().unstack()
print("\nCantidad de viajes por día de la semana:")
print(viajes_dia_usuario)

df_limpio.to_csv(r"D:\Phyton_Analist\Proyect_cyclist\cyclistic_limpio_para_tableau.csv", index=False)

df_limpio.to_csv(r"D:\Phyton_Analist\Proyect_cyclist\cyclistic_limpio_para_tableau.csv", index=False)

if not df_limpio.empty:
    ruta_exportacion = r"D:\Phyton_Analist\Proyect_cyclist\cyclistic_limpio_para_tableau.csv"
    print(f"Exportando {len(df_limpio):,} filas...")
    
    # Exportar a CSV (esto puede tardar unos minutos por el tamaño)
    df_limpio.to_csv(ruta_exportacion, index=False)
    
    print(f"¡Exportación completada! Archivo listo en: {ruta_exportacion}")
else:
    print("Error: df_limpio está vacío. Vuelve a ejecutar la celda de limpieza de datos.")

import pandas as pd

# Suponiendo que tu dataframe original (después de cargar el Parquet) se llama 'df'
# 1. Asegurar que las fechas son formato datetime
df['started_at'] = pd.to_datetime(df['started_at'])
df['ended_at'] = pd.to_datetime(df['ended_at'])

# 2. Recalcular 'ride_length' en minutos (esto es crucial)
df['length_day'] = (df['ended_at'] - df['started_at']).dt.total_seconds() / 60

# 3. Eliminar filas donde la duración sea nula o negativa
df_limpio = df.dropna(subset=['length_day'])
df_limpio = df_limpio[df_limpio['length_day'] > 1]

# 4. Verificar que ahora sí hay datos numéricos (debe imprimir promedios, no NaN)
print(df_limpio['length_day'].describe())

# Tomamos una muestra para que Tableau sea súper rápido
df_muestra = df_limpio.sample(frac=0.10, random_state=42)

ruta_muestra = r"D:\Phyton_Analist\Proyect_cyclist\cyclistic_limpio_para_tableau.csv"

# Exportamos usando punto y coma para evitar problemas regionales
df_muestra.to_csv(ruta_muestra, index=False, sep=';')
print("Archivo exportado correctamente.")

# Tomamos una muestra para que Tableau sea súper rápido
df_muestra = df_limpio.sample(frac=0.10, random_state=42)

ruta_muestra = r"D:\Phyton_Analist\Proyect_cyclist\cyclistic_limpio_para_tableau.csv"

# Exportamos usando punto y coma para evitar problemas regionales
df_muestra.to_csv(ruta_muestra, index=False, sep=';')
print("Archivo exportado correctamente.")

import pandas as pd
import numpy as np

# 1. Cargar el archivo completo original (asegúrate de que la ruta sea correcta)
ruta_parquet = r"D:\Phyton_Analist\Proyect_cyclist\cyclistic_12_meses.parquet"
df = pd.read_parquet(ruta_parquet)

print(f"Filas originales cargadas: {len(df):,}")

# 2. Asegurar tipos de datos correctos para las fechas
df['started_at'] = pd.to_datetime(df['started_at'])
df['ended_at'] = pd.to_datetime(df['ended_at'])

# 3. Calcular la duración exacta del viaje en minutos (asegurando que sea float numérico)
df['ride_length'] = (df['ended_at'] - df['started_at']).dt.total_seconds() / 60

# 4. Calcular el día de la semana (1 = Domingo, 7 = Sábado)
day_of_week_pandas = df['started_at'].dt.dayofweek
df['day_of_week'] = (day_of_week_pandas + 2) % 7
df['day_of_week'] = df['day_of_week'].replace(0, 7)

# 5. Limpieza estricta: eliminar nulos y viajes menores a 1 minuto o negativos
df_limpio = df.dropna(subset=['ride_length', 'member_casual', 'start_station_name'])
df_limpio = df_limpio[df_limpio['ride_length'] >= 1]
df_limpio = df_limpio[~df_limpio['start_station_name'].str.contains('Test|HQ QR', na=False, case=False)]

print(f"Filas totales después de la limpieza: {len(df_limpio):,}")

# 6. Guardar como CSV optimizado usando comas (estándar de Tableau) y punto decimal estándar
ruta_salida = r"D:\Phyton_Analist\Proyect_cyclist\cyclistic_completo_tableau.csv"
df_limpio.to_csv(ruta_salida, index=False, decimal='.')

print(f"¡Archivo completo guardado exitosamente en: {ruta_salida}")

