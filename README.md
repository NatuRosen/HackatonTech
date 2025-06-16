Guardián Clima ITBA - 

Este proyecto es una aplicación de consola escrita en Python. Permite consultar el clima actual en cualquier ciudad, país o región del mundo, ver tu historial de consultas, obtener estadísticas sobre el clima y recibir consejos de vestimenta generados por inteligencia artificial según la temperatura.

¿Qué hay que hacer para que funcione el programa ? Checklist 

Primer Paso: Instalar Visual Studio Code 
En caso de no tener la aplicación descargada dirigirse a https://code.visualstudio.com/ e instalarla para su dispositivo
Segundo Paso : Instalar Python 
Una vez dentro de la aplicación de Visual Studio Code dirigirse a la parte de Extensiones y descargar Python dentro de la aplicación. 
También hay que instalar por separado Python así la computadora puede interpretar el lenguaje en caso de no tenerlo instalado dirigirse hacia : https://www.python.org/downloads/ 
Tercer Paso : Descargar el archivo app.py 	
Una vez descargado el archivo app.py abrirlo con la aplicación de Visual Studio Code
Cuarto paso : Descargar las librerias necesarias 
Para que esta aplicación funcione correctamente hay que descargar las librerías de Google generative AI. Escribir lo siguiente en la consola para descargar las librerias necesarias :  pip install requests google-generativeai
Quinto paso : Obtener las API,s Keys (llaves) 
IMPORTANTE: Todas las APIs utilizadas en este proyecto son gratuitas, si en alguna aplicación o página web te pide datos personales o bancarios no los ingreses, está en la página equivocada. 
Obtener las llaves de Open Weather Map y las de Gemini AI 
Para las llaves de Open Weather Map dirigirse a : https://home.openweathermap.org/users/sign_up 
y registrarse o ingresar con su cuenta. 
Una vez dentro apretar el botón que dice API Keys y copiar la llave. Luego volver a Visual Studio Code y reemplazar donde dice : 
OPENWEATHER_API_KEY = “ tu llave aquí ” 
Para las llaves de Gemini AI ir al enlace : https://aistudio.google.com/prompts/new_chat y registrase con su cuenta. Luego arriba a la derecha hay un botón que dice “Get API Key” / “Obtener la clave API” y reemplazarla en el código donde dice :  
GEMINI_API_KEY = " tu llave aquí "
Sexto paso : Ejecutar el programa 
Una vez hecho todo lo anterior volver a la aplicación de Visual Studio Code y dentro de la aplicacion, arriba a la derecha donde dice "File"/"Archivo" ir a donde dicec abrir carpeta. Dentro de tus archivos en la seccion de documentos cliquear el archivo de HackatonTech y dentro del archivo de HackatonTech abrir el ProyectoGuardianClima. Para ejecutarlo hay que escribir en la terminal : python app.py o cliquear el boton de arriba a la derecha para ejecutarlo. 


AUTORES : 

José Ignacio Aldaco

Joaquín Nicolás Dominguez Gaviola

Santiago Ranftl

Santiago Ramón Garriga Zimmermann

Natan Jonas Rosenhain
