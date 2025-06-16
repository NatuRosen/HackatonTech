GuardiánClima ITBA

GuardiánClima ITBA es una aplicación de consola multifuncional desarrollada en Python. Permite a los usuarios obtener datos meteorológicos en tiempo real, gestionar un historial de consultas, analizar estadísticas de uso y recibir consejos de vestimenta personalizados, generados por Inteligencia Artificial, basados en las condiciones climáticas.
Este proyecto fue diseñado como una demostración práctica de la integración de conceptos de Programación, Ciberseguridad, Análisis de Datos, Conectividad en la Nube e Inteligencia Artificial.

Core Features
- Consulta de Clima en Tiempo Real: Obtén datos actualizados de temperatura, sensación térmica, humedad y viento para cualquier ciudad del mundo a través de la API de OpenWeatherMap.
- Historial de Consultas: Guarda automáticamente cada consulta en un archivo .csv, permitiendo llevar un registro personal y global.
- Estadísticas de Uso: Analiza el historial global para obtener métricas como la ciudad más consultada y la temperatura promedio de todas las búsquedas.
- Consejero de Vestimenta por IA: Utiliza la API de Google Gemini para recibir recomendaciones de ropa prácticas y adaptadas al clima de la ciudad que elijas.
- Gestión de Usuarios: Un sistema simulado de registro e inicio de sesión para personalizar la experiencia.

Tecnologías Utilizadas
- Lenguaje: Python 3
- APIs Externas:
    - OpenWeatherMap para datos climáticos.
    - Google Gemini para la generación de texto por IA.
- Librerías Principales: requests, google-generativeai.

Prerrequisitos
- Antes de comenzar, asegúrate de tener instalado Python 3.7 o superior en tu sistema.
    Para verificar tu versión de Python ejecuta el siguiente comando en la consola:
        python --version

En caso de no tener Python instalado, puedes descargarlo desde el sitio web oficial:
- https://www.python.org/downloads/

También se recomienda un editor de código como Visual Studio Code para ñograr ejecutar usar el programa correctamente. Puede descargarse desde el siguiente link:
- https://code.visualstudio.com/

Instalar las Dependencias
 - Instala las librerías de Python necesarias ejecutando el siguiente comando en tu terminal.
    pip install requests google-generativeai

Configuración de las Claves API (Método Seguro)
- La aplicación requiere credenciales para acceder a los servicios de OpenWeatherMap y Google Gemini. Para manejarlas de forma segura sin exponerlas en el código fuente, se utiliza un archivo de entorno.
    - OpenWeatherMap API Key: Se puede obtener registrándose en el sitio web de OpenWeatherMap y accediendo a la sección "API keys" del panel de usuario.
        https://openweathermap.org/api
    - Gemini API Key: Se puede generar en Google AI Studio tras iniciar sesión con una cuenta de Google.
        https://aistudio.google.com/app/apikey

Añadir las claves API al archivo .env:
- Abra el archivo .env con un editor de texto e inserte las siguientes líneas, reemplazando "TU_LLAVE_AQUI" con sus claves reales obtenidas de los respectivos servicios.
    OPENWEATHER_API_KEY="TU_LLAVE_DE_OPENWEATHERMAP_AQUI"
    GEMINI_API_KEY="TU_LLAVE_DE_GEMINI_AQUI"

Cómo Ejecutar la Aplicación
- Una vez completada la instalación y configuración, puedes iniciar la aplicación desde tu terminal, asegurándote de estar en el directorio raíz del proyecto.
    python app.py
Al ejecutar el comando, se presentará el menú principal de acceso en la consola, donde podrás registrarte o iniciar sesión.

Estructura del Proyecto
- Cuando ejecutes la aplicación, se crearán automáticamente los siguientes archivos en el mismo directorio:
    - app.py: El script principal que contiene toda la lógica de la aplicación.
    - usuarios_simulados.csv: Almacena los nombres de usuario y contraseñas (en texto plano, con fines educativos).
    - historial_global.csv: Guarda un registro de todas las consultas de clima realizadas por todos los usuarios.

Al iniciar, la aplicación presenta el Menú de Acceso con las siguientes opciones:
- Iniciar Sesión: Permite a un usuario ya registrado acceder al sistema mediante su nombre de usuario y contraseña.
- Registrar Nuevo Usuario: Inicia el flujo para la creación de una nueva cuenta, solicitando un nombre de usuario y una contraseña que debe cumplir con criterios de seguridad.
- Salir de la Aplicación: Cierra el programa.

Tras una autenticación exitosa, el usuario accede al Menú Principal, que contiene las siguientes funcionalidades:
- Consultar Clima Actual y Guardar en Historial: Solicita el nombre de una ciudad, muestra el clima actual y guarda la consulta en los archivos de historial.
- Ver Mi Historial Personal de Consultas por Ciudad: Permite al usuario revisar sus consultas previas para una ciudad específica.
- Estadísticas Globales de Uso: Muestra datos agregados de todas las consultas realizadas, como la ciudad más buscada y la temperatura promedio.
- Consejo IA: ¿Cómo Me Visto Hoy?: Utiliza la IA de Gemini para generar una recomendación de vestimenta basada en el clima de una ciudad.
- Acerca De...: Muestra información sobre el proyecto y sus desarrolladores.
- Cerrar Sesión: Finaliza la sesión del usuario actual y regresa al Menú de Acceso.

Autores
- Este proyecto fue desarrollado por:
    - José Ignacio Aldaco
    - Joaquín Nicolás Dominguez Gaviola
    - Santiago Ranftl
    - Santiago Ramón Garriga Zimmermann
    - Natan Jonas Rosenhain