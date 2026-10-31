Caso de Estudio Cyclistic Bike-Share: Estrategia de Conversión de Usuarios Ocasionales a Miembros Anuales

1. Resumen Ejecutivo (Answer-First)

Para maximizar el crecimiento rentable de Cyclistic mediante la conversión de ciclistas ocasionales en miembros anuales, la empresa debe pivotar su enfoque desde el marketing masivo de fin de semana hacia la captura quirúrgica de usuarios frecuentes de bicicletas eléctricas y commuters híbridos.

Este análisis demuestra que el mayor potencial de conversión no reside en el turista de fin de semana, sino en el millón de viajes casuales que ocurren de lunes a viernes, fuertemente apalancados por una alta adopción de la flota eléctrica.

2. El Problema (Ask)

El equipo directivo y financiero de Cyclistic determinó que las membresías anuales son sustancialmente más rentables que los pases de viaje único o de día completo. El objetivo comercial de este proyecto es analizar el comportamiento diferencial entre los miembros anuales y los usuarios ocasionales sobre los datos históricos de 12 meses, para diseñar estrategias de conversión y campañas de marketing digital basadas en evidencia.

3. Datos y Limpieza (Prepare & Process)

El proyecto implicó la extracción, consolidación y limpieza de un gran volumen de datos transaccionales generados por una red de 5,824 bicicletas y 692 estaciones en Chicago.

Herramientas: Python (Pandas) para procesamiento; Tableau para visualización.

Volumen: Se procesaron 6.17 millones de registros iniciales, aplicando reglas estrictas de depuración (eliminación de nulos, viajes < 1 minuto, y registros de mantenimiento) para obtener un dataset final auditado de 4,810,648 viajes válidos.

Resolución de Restricciones (PII): Debido a normativas de privacidad, no se contaba con información de identificación personal (PII) ni tarjetas de crédito para rastrear usuarios únicos. Este obstáculo se resolvió diseñando un modelo de proxies comportamentales (cruzando día, hora, duración, tipo de flota y estaciones residenciales/laborales) para aislar a los residentes locales de los turistas de paso.

4. Análisis y Hallazgos Clave (Analyze)

El análisis descriptivo sobre los casi 5 millones de registros reveló tres hallazgos contraintuitivos que rompen con los supuestos tradicionales del negocio:

El 63.03% de los viajes ocasionales ocurre de lunes a viernes: De 1,682,831 viajes casuales, 1,060,724 suceden en días hábiles. Existe un "segmento oculto" de trabajadores híbridos y residentes locales que utilizan el servicio de manera constante entre semana.

Pico de adopción eléctrica a mitad de semana: La bicicleta eléctrica (electric_bike) es el verdadero motor de adquisición. Los usuarios ocasionales la eligen en el 67.4% de sus trayectos, alcanzando un récord de 71.20% de adopción los miércoles (una brecha de +10.0 pp frente a los miembros anuales).

Asimetría en la duración del viaje (+79.8%): Los usuarios ocasionales realizan viajes significativamente más largos (23.2 minutos en promedio frente a los 12.9 minutos de los miembros). Esta duración prolongada expone al usuario casual a fuertes recargos por minuto en pases individuales.

5. Visualización (Share)

Los hallazgos han sido consolidados en un panel ejecutivo interactivo, diseñado para facilitar la toma de decisiones del Comité Directivo.

Dashboard en Tableau Public: [Inserta aquí tu enlace a Tableau Public]

6. Recomendaciones Estratégicas (Act)

Para convertir la fricción tarifaria del usuario casual en suscripciones anuales completas (protegiendo el margen unitario de las E-Bikes y la disponibilidad de flota), se proponen tres iniciativas respaldadas por un protocolo de pruebas A/B de 90 días:

In-App Instant Ride-Credit Rollover: Bonificar el 100% del viaje recién pagado (para trayectos >20 min) como un crédito inmediato hacia la Membresía Anual a través de un pop-up en la aplicación, capitalizando el momento de "dolor de pago".

E-Bike Commuter Pass ($0 Unlock Fee): Eliminar la tarifa de desbloqueo eléctrico para miembros anuales (manteniendo la tarifa por minuto reducida), apoyado por un sistema de Rebalanceo Gamificado donde los usuarios ganan créditos si devuelven las bicis en estaciones con déficit matutino.

Programa Weekend-to-Weekday Bridge: Enfoque en estaciones residenciales para ofrecer un mes de prueba que incluye reserva anticipada de 15 minutos en la app y 2 pases de invitado anuales, transformando el hábito recreativo del sábado en uso laboral el lunes.

7. Entregable Final

La presentación ejecutiva completa, detallando la metodología, el análisis de economía unitaria (Unit Economics) y el diseño experimental (Test A/B), se encuentra disponible en formato PDF en la carpeta /deliverables de este repositorio.

Ver Presentación Ejecutiva (PDF)
