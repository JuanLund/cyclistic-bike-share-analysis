# PROYECTO 1: Caso de Estudio Cyclistic Bike-Share
**Autor:** Juan Lund — Business & Operations Data Analyst  
**Stack Técnico:** Python (Pandas, NumPy) · Tableau Public · Diseño Experimental A/B  
**Volumen Procesado:** 6,171,785 registros brutos $\rightarrow$ 4,810,648 viajes certificados (12 meses)

---

## 1. Síntesis Ejecutiva (Answer-First)
Para maximizar el crecimiento rentable de Cyclistic mediante la conversión de ciclistas ocasionales en miembros anuales, la empresa debe **pivotar su enfoque desde el marketing masivo de fin de semana hacia la captura quirúrgica de usuarios frecuentes de bicicletas eléctricas y *commuters* híbridos**.

El análisis de los **4,810,648 viajes válidos** de los últimos 12 meses demuestra tres realidades contraintuitivas que redefinen la estrategia comercial:
1. **El 63.03% de los viajes ocasionales ocurre de lunes a viernes ($1,060,724$ de $1,682,831$ viajes):** Aunque el sábado presenta el pico diario individual ($353,661$ viajes), casi dos tercios del volumen casual anual se genera en días laborables (con un piso constante de $\sim 195,000$ a $209,000$ viajes diarios de lunes a jueves). Este segmento representa trabajadores híbridos o residentes locales con el mayor potencial de conversión inmediata.
2. **La bicicleta eléctrica (`electric_bike`) es el verdadero motor de adquisición casual (hasta $71.20\%$ de adopción):** Los usuarios ocasionales eligen bicicletas eléctricas en el **$67.4\%$ ponderado de sus viajes anuales** —alcanzando picos del **$70.36\%$ el martes, $71.20\%$ el miércoles y $70.40\%$ el jueves**—, superando sistemáticamente la tasa de uso eléctrico de los miembros anuales ($60.5\%$ ponderado; brecha de hasta $+10.04\text{ pp}$).
3. **Los viajes ocasionales son un $79.8\%$ más largos ($23.2\text{ min}$ vs. $12.9\text{ min}$):** Al combinar trayectos casi $1.8\times$ más extensos con el uso intensivo de flota eléctrica, el usuario ocasional recurrente sufre una alta fricción económica por tarifas de desbloqueo y cargos por minuto. Convertir ese gasto recién realizado en un **crédito inmediato hacia la membresía anual** en la app móvil es la palanca digital de mayor retorno sobre la inversión (ROI).

---

## 2. Fase 1 & 2: Preguntar (Ask) y Preparar (Prepare)

### 2.1 Tarea Comercial y Stakeholders
* **Tarea Comercial:** Analizar los datos históricos de viajes de los últimos 12 meses para identificar diferencias conductuales entre miembros anuales y ciclistas ocasionales, diseñando una estrategia digital respaldada en datos que maximice la conversión a membresías anuales sin erosionar el margen operativo.
* **Stakeholders Principales:**
  * **Lily Moreno:** Directora de Marketing y responsable directa de las campañas digitales.
  * **Comité Ejecutivo de Cyclistic:** Órgano directivo detallista encargado de aprobar la inversión y validar la viabilidad operativa.
  * **Equipo de Análisis de Marketing:** Equipo técnico encargado de la gobernanza de datos y medición de pruebas A/B.

### 2.2 Parámetros Operativos y Gobernanza (ROCCC & PII)
* **Infraestructura:** Red de **5,824 bicicletas** y **692 estaciones** en Chicago ($\sim 30\%$ de uso por *commuting* laboral y $\sim 8\%$ de adopción en opciones de flota asistida/inclusiva).
* **Licencia y Credibilidad:** Datos públicos históricos proporcionados por Motivate International Inc. bajo licencia oficial. Cumplen con el estándar **ROCCC** (Reliable, Original, Comprehensive, Current, Cited).
* **Restricción de Privacidad (Sin PII):** Por normativas de privacidad, el dataset no incluye identificadores personales (IDs de usuario ni tarjetas de crédito). La recurrencia se modeló mediante **proxies espacio-temporales** (franja horaria, día laboral vs. fin de semana, tipo de bicicleta y estaciones).

---

## 3. Fase 3: Procesar (Process) — Pipeline en Python (Pandas)

### 3.1 Embudo de Auditoría y Limpieza de Datos
* **Registros brutos unificados (12 archivos CSV mensuales):** $6,171,785$ filas.
* **Reglas de depuración aplicadas:**
  1. Estandarización de `started_at` y `ended_at` a formato `datetime64`.
  2. Cálculo de `ride_length` en minutos decimales: $\frac{\text{ended\_at} - \text{started\_at}}{60}$.
  3. Creación de `day_of_week` ajustado al estándar comercial ($1 = \text{Domingo}$ a $7 = \text{Sábado}$).
  4. Eliminación de valores nulos críticos (`ride_length`, `member_casual`, `start_station_name`).
  5. Exclusión de viajes $< 1\text{ minuto}$ (falsos desbloqueos o fallos de anclaje) y pruebas operativas en estaciones `Test` o `HQ QR`.
* **Registros descartados por ruido operativo:** $1,361,137$ filas ($22.05\%$).
* **Población final auditada:** **$4,810,648$ viajes certificados** ($3,127,817$ de miembros anuales [$65.02\%$] y $1,682,831$ de ciclistas ocasionales [$34.98\%$]).

### 3.2 Script Maestro de Extracción, Limpieza y Exportación (`cyclistic_pipeline.py`)
```python
import pandas as pd
import numpy as np
import requests
import zipfile
import io

# ==============================================================================
# PASO 1: DESCARGA AUTOMATIZADA Y CONSOLIDACIÓN DE 12 MESES (PARQUET)
# ==============================================================================
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

df_anual = pd.concat(lista_df, ignore_index=True)
ruta_parquet = r"D:\Phyton_Analist\Proyect_cyclist\cyclistic_12_meses.parquet"
df_anual.to_parquet(ruta_parquet, index=False)
print(f"Total de filas brutas consolidadas: {len(df_anual):,}")

# ==============================================================================
# PASO 2: LIMPIEZA ESTRICTA, TRANSFORMACIÓN Y EXPORTACIÓN PARA TABLEAU
# ==============================================================================
df = pd.read_parquet(ruta_parquet)

# 1. Asegurar formato datetime
df['started_at'] = pd.to_datetime(df['started_at'])
df['ended_at'] = pd.to_datetime(df['ended_at'])

# 2. Calcular duración exacta del viaje en minutos (float)
df['ride_length'] = (df['ended_at'] - df['started_at']).dt.total_seconds() / 60.0

# 3. Calcular día de la semana (1 = Domingo, 7 = Sábado)
day_of_week_pandas = df['started_at'].dt.dayofweek
df['day_of_week'] = (day_of_week_pandas + 2) % 7
df['day_of_week'] = df['day_of_week'].replace(0, 7)

# 4. Filtrado de integridad (nulos, viajes < 1 min y estaciones de prueba)
df_limpio = df.dropna(subset=['ride_length', 'member_casual', 'start_station_name']).copy()
df_limpio = df_limpio[df_limpio['ride_length'] >= 1.0]
df_limpio = df_limpio[~df_limpio['start_station_name'].str.contains('Test|HQ QR', na=False, case=False)]

print(f"Filas certificadas tras limpieza: {len(df_limpio):,}")
print(f"Filas eliminadas: {len(df) - len(df_limpio):,}")

# 5. Resumen estadístico de verificación
print("\n--- DURACIÓN PROMEDIO POR TIPO DE USUARIO (MINUTOS) ---")
print(df_limpio.groupby('member_casual')['ride_length'].mean())

# 6. Exportación optimizada para Tableau Public (estándar internacional)
ruta_salida = r"D:\Phyton_Analist\Proyect_cyclist\cyclistic_completo_tableau.csv"
df_limpio.to_csv(ruta_salida, index=False, decimal='.')
print(f"Archivo exportado exitosamente en: {ruta_salida}")
```

---

## 4. Fase 4: Analizar (Analyze) — Tablas Maestras de Resultados

### 4.1 Tabla Maestra de Comportamiento Semanal y Adopción de Flota Eléctrica
| Día de la Semana | Viajes Miembros (`member`) | Viajes Ocasionales (`casual`) | % E-Bike Miembros | % E-Bike Ocasionales | Brecha E-Bike (pp) | Duración Media Casual vs. Member | Diagnóstico Operativo y Comercial |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Lunes** | $444,961$ | $195,794$ | $59.84\%$ | $67.27\%$ | $+7.43\text{ pp}$ | $20.4\text{ vs. }12.1\text{ min}$ | Inicio de tracción laboral; piso casual sólido. |
| **Martes** | **$510,456$** | $194,345$ | $60.67\%$ | $70.36\%$ | $+9.69\text{ pp}$ | $17.5\text{ vs. }11.9\text{ min}$ | **Pico absoluto de miembros**; alta demanda eléctrica. |
| **Miércoles** | $509,025$ | $196,525$ | $61.16\%$ | **$71.20\%$** | **$+10.04\text{ pp}$** | $16.7\text{ vs. }11.8\text{ min}$ | **Récord de adopción E-Bike casual** (*commuter* híbrido). |
| **Jueves** | $493,255$ | $208,996$ | $61.71\%$ | $70.40\%$ | $+8.69\text{ pp}$ | $17.8\text{ vs. }11.9\text{ min}$ | Consolidación laboral previa al fin de semana. |
| **Viernes** | $457,571$ | $265,064$ | $61.50\%$ | $68.12\%$ | $+6.62\text{ pp}$ | $20.0\text{ vs. }12.4\text{ min}$ | Día bisagra: transición entre transporte y ocio. |
| **Sábado** | $387,927$ | **$353,661$** | $59.45\%$ | $64.15\%$ | $+4.70\text{ pp}$ | $23.2\text{ vs. }13.8\text{ min}$ | **Pico individual casual**; uso recreativo extendido. |
| **Domingo** | $324,622$ | $268,446$ | $58.30\%$ | $63.40\%$ | $+5.10\text{ pp}$ | $23.6\text{ vs. }13.7\text{ min}$ | Cierre de fin de semana con trayectos largos. |
| **Total / Promedio** | **$3,127,817$ ($65.0\%$)** | **$1,682,831$ ($35.0\%$)** | **$60.5\%$** | **$67.4\%$** | **$+6.90\text{ pp}$** | **$23.2\text{ vs. }12.9\text{ min}$** | **$63.03\%$ del volumen casual ocurre de Lunes a Viernes.** |

### 4.2 Matriz de Arquetipos de Usuarios Ocasionales (Segmentación sin PII)
| Arquetipo Casual | Prioridad CAC | Volumen Anual Estimado | Regla Proxy en Datos | Táctica Comercial Asignada |
| :--- | :---: | :---: | :--- | :--- |
| **1. Commuter Híbrido** | **Alta (Prioridad 1)** | $\sim 795,660$ viajes (Lun–Jue) | Viajes entre semana en horas pico ($7\text{–}9\text{h}$, $16\text{–}19\text{h}$), uso de `electric_bike` ($>70\%$), duración $15\text{–}20\text{ min}$. | *E-Bike Commuter Pass* ($0 desbloqueo eléctrico) + *Instant Ride-Credit Rollover*. |
| **2. Residente Recreativo & Flota Asistida (8%)** | **Media-Alta (Prioridad 2)** | $\sim 550,000$ viajes (Vie–Dom recurrente) | Estaciones residenciales/parques, trayectos $>20\text{ min}$ y usuarios del $8\%$ de flota inclusiva. | *Instant Ride-Credit Rollover* al finalizar viajes $>20\text{ min}$ + *Weekend-to-Weekday Bridge*. |
| **3. Turista de Paso** | **Baja (Exclusión CAC)** | $\sim 337,000$ viajes (Sáb–Dom aislados) | Estaciones turísticas/costeras, pases de día completo, viajes $>35\text{ min}$ en `classic_bike`. | **No invertir presupuesto de conversión anual** (LTV nulo para membresía anual). |

---

## 5. Fase 5: Compartir (Share) — Arquitectura en Tableau Public
* **Título del Dashboard:** `Cyclistic Bike-Share: Análisis Comparativo de Usuarios (4.81M Viajes)`
* **Estructura Visual (3 Paneles Interactivos):**
  1. **Superior (Tendencia Semanal de Volumen):** Gráfico de líneas comparando `member` vs. `casual` de lunes a domingo (destacando la meseta laboral casual de $\sim 195\text{k–}209\text{k}$ viajes y el pico de martes en miembros con $510,456$).
  2. **Inferior Izquierdo (Curva de Penetración de Flota Eléctrica):** Gráfico comparativo que evidencia la brecha de hasta $+10.04\text{ pp}$ los miércoles ($71.20\%$ en ocasionales vs. $61.16\%$ en miembros).
  3. **Inferior Derecho (Duración Promedio del Viaje):** Gráfico de barras contrastando los $23.2\text{ min}$ de los ciclistas ocasionales frente a los $12.9\text{ min}$ de los miembros anuales ($+79.8\%$), con línea de referencia de umbral tarifario en el minuto 15.

---

## 6. Fase 6: Actuar (Act) — Plan Estratégico y Protocolo Experimental A/B

### 6.1 Las 3 Iniciativas Comerciales y Operativas
1. **Iniciativa 1 — Conversión In-App "Reembolso del Primer Viaje" (*Instant Ride-Credit Rollover*):**
   * *Mecanismo:* Al finalizar un viaje casual $>20\text{ minutos}$ o en `electric_bike`, la app despliega una oferta con temporizador de 15 minutos que bonifica el $100\%$ del costo de ese viaje como descuento directo si el usuario adquiere la Membresía Anual en ese instante.
   * *Finanzas:* Elimina el dolor de pago inmediato (*point-of-pain*) sin crear pases de fin de semana que canibalicen el flujo de caja anual.
2. **Iniciativa 2 — Posicionamiento "Membresía Anual = E-Bike Commuter Pass" con Rebalanceo Gamificado:**
   * *Mecanismo:* Campaña digital hiper-segmentada en distritos laborales y residenciales destacando **"$0 Tarifa de Desbloqueo en Bicicletas Eléctricas todo el año"**.
   * *Salvaguarda Operativa (5,824 bicicletas / 692 estaciones):* Otorga créditos de minutos eléctricos cuando el usuario estaciona la `electric_bike` en estaciones deficitarias ("Estaciones Verdes") antes de las 8:30 AM, evitando el desabastecimiento (*stock-out*) de baterías y reduciendo el costo logístico de camiones.
3. **Iniciativa 3 — Puente "Weekend-to-Weekday" y Captura de Flota Asistida (8%):**
   * *Mecanismo:* Secuencia automatizada por push/email los domingos a las 19:00h para usuarios casuales del fin de semana, ofreciendo desbloqueos eléctricos bonificados de lunes a jueves durante 14 días al suscribirse al plan anual, incluyendo beneficios prioritarios de reserva para el $8\%$ de usuarios de bicicletas asistidas.

### 6.2 Matriz de Experimentación A/B (8 Semanas)
| Iniciativa | Grupo Control vs. Tratamiento | Muestra Objetivo | KPI Primario de Éxito | Métrica Guarda-Riel (Guardrail) |
| :--- | :--- | :---: | :--- | :--- |
| **1. Instant Ride-Credit Rollover** | **Control:** Pantalla estándar de recibo.<br>**Tratamiento:** Pop-up con crédito del $100\%$ del viaje hacia membresía anual. | $100,000$ viajes casuales ($>20\text{ min}$ o E-Bike) | Tasa de conversión a Membresía Anual dentro de las 24h ($\text{Meta: }+1.8\%\text{ a }+2.5\%$). | Margen neto de adquisición en el Mes 1 y tasa de reembolso/disputa. |
| **2. E-Bike Commuter Pass + Rebalanceo** | **Control:** Anuncio genérico de membresía.<br>**Tratamiento:** Propuesta de ahorro en E-Bike + créditos por Estación Verde. | $250,000$ impresiones geocercadas (Lun–Jue) | Costo de Adquisición de Cliente (CAC) y conversión en días hábiles. | **Tasa de disponibilidad de E-Bikes** en horas pico ($>85\%$ en estaciones Top 100). |
| **3. Puente Weekend-to-Weekday** | **Control:** Newsletter mensual estándar.<br>**Tratamiento:** Push dominical personalizado con reto de uso laboral. | $80,000$ usuarios casuales de fin de semana | Incremento en viajes realizados entre lunes y jueves y conversión a plan anual. | Tasa de desuscripción (*opt-out*) de notificaciones push ($<1.5\%$). |