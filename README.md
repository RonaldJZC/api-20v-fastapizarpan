1. Para qué se puede usar Python en lo que respecta a datos. Dar 5 casos y explicar brevemente
Python se puede usar para casi todo lo relacionado con datos, porque tiene librerías muy potentes.
Algunos casos:
1.	Análisis de datos → usando Pandas o NumPy se puede limpiar, procesar y analizar grandes volúmenes de información (por ejemplo, analizar el historial de mantenimientos de equipos médicos).
2.	Visualización → con Matplotlib o Seaborn se crean gráficos que permiten entender tendencias y comportamientos en los datos.
3.	Machine Learning → usando Scikit-learn o TensorFlow se pueden crear modelos predictivos, por ejemplo, para anticipar fallas en equipos.
4.	Automatización de reportes → se pueden generar informes automáticos (PDF, Excel, etc.) a partir de bases de datos o sensores.
5.	Integración con bases de datos → Python puede conectarse con SQL, MongoDB o APIs para recolectar y combinar información de diferentes fuentes.
------------------------------------------------------------------
2. ¿Cómo se diferencian Flask de Django? Argumentar.
Ambos son frameworks web de Python, pero tienen enfoques distintos:
•	Flask es más ligero y flexible, ideal para proyectos pequeños o cuando uno quiere controlar cada parte del desarrollo. Por ejemplo, lo usé para crear una API que registra mantenimientos médicos.
•	Django es más estructurado y completo, ya trae autenticación, panel de administración, ORM, etc. Es más útil para proyectos grandes o empresariales donde se necesita escalabilidad.
En resumen:
Flask = libertad y simplicidad.
Django = estructura y todo integrado.
---------------------------------------------------------------------
3. ¿Qué es un API? Explicar en sus propias palabras
Un API (Interfaz de Programación de Aplicaciones) es como un puente que permite que dos sistemas diferentes se comuniquen entre sí.
Por ejemplo, una app web puede usar un API para pedir datos a una base de datos sin tener acceso directo.
En mi caso, usé FastAPI para crear un servicio que recibe datos de equipos médicos y los guarda en MongoDB, permitiendo que otras apps consulten esa información fácilmente.
---------------------------------------------------------------------
4. ¿Cuál es la principal diferencia entre REST y WebSockets?
•	REST se basa en peticiones HTTP normales (como GET, POST, PUT, DELETE). Cada solicitud es independiente y se usa mucho para APIs tradicionales.
•	WebSockets permite una comunicación en tiempo real, donde el servidor y el cliente mantienen una conexión abierta (por ejemplo, en chats o monitoreo en vivo de equipos).
Entonces:
REST = comunicación puntual.
WebSockets = comunicación continua y en tiempo real.
---------------------------------------------------------------------------
5. Describir un ejemplo de API comercial y cómo funciona – usar otros ejemplos no vistos en el curso.
Un ejemplo es la API de OpenWeatherMap.
Permite obtener datos del clima de cualquier ciudad del mundo. Uno se registra, obtiene una “API key” y realiza peticiones como:
https://api.openweathermap.org/data/2.5/weather?q=Lima&appid=TU_API_KEY
El servidor devuelve un JSON con la temperatura, humedad, presión, etc.
Esto se puede integrar, por ejemplo, en una aplicación hospitalaria para ajustar automáticamente la climatización de ambientes donde se guardan equipos sensibles.
