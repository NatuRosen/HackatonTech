# -*- coding: utf-8 -*-

# ==============================================================================
#  GuardiánClima ITBA - Versión 1.0
#  Proyecto Integrador
# ==============================================================================
#
#  Este script contiene la aplicación de consola completa, incluyendo:
#  - Gestión de usuarios (simulada e insegura, con fines educativos).
#  - Consulta de clima vía API (OpenWeatherMap).
#  - Historial de consultas global y personal.
#  - Estadísticas de uso.
#  - Consejo de vestimenta por IA (Google Gemini).
#
#  Para ejecutar:
#  1. Instalar las librerías necesarias:
#     pip install requests google-generativeai
#
#  2. Configurar las API Keys en las siguientes constantes:
#     - OPENWEATHER_API_KEY
#     - GEMINI_API_KEY
#
# ==============================================================================

import csv
import os
import re
import requests
import google.generativeai as genai
from datetime import datetime
from collections import Counter

# --- CONFIGURACIÓN DE API KEYS ---
# ¡IMPORTANTE! Reemplazar con tus propias claves API.
OPENWEATHER_API_KEY = "6c444f6b4dbeab835f5ec48e70463b08"
GEMINI_API_KEY = "AIzaSyAh3HljDHn8KtMmLrNgQZ9lXEFXcvH-gG4"

# --- Constantes y Configuración Global ---
NOMBRE_ARCHIVO_USUARIOS = "usuarios_simulados.csv"
NOMBRE_ARCHIVO_HISTORIAL = "historial_global.csv"

# Configuración de la API de IA (Gemini)
try:
    if GEMINI_API_KEY != "TU_API_KEY_AQUI_GEMINI":
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
    else:
        model = None
except Exception as e:
    print(f"[ADVERTENCIA] No se pudo configurar la API de Gemini. Error: {e}")
    model = None


# ==============================================================================
#  SECCIÓN 1: GESTIÓN DE USUARIOS Y ACCESO (Ciberseguridad, Programación)
# ==============================================================================

def inicializar_archivo(nombre_archivo, cabeceras):
    """Función genérica para crear un archivo CSV con cabeceras si no existe."""
    if not os.path.exists(nombre_archivo):
        with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as archivo_csv:
            writer = csv.writer(archivo_csv)
            writer.writerow(cabeceras)

def validar_contrasena(contrasena):
    """
    [CIBERSEGURIDAD] Valida la contraseña según 3 criterios de seguridad.
    """
    errores = []
    if len(contrasena) < 8:
        errores.append("Debe tener al menos 8 caracteres.")
    if not re.search(r'[A-Z]', contrasena):
        errores.append("Debe contener al menos una mayúscula.")
    if not re.search(r'[0-9]', contrasena):
        errores.append("Debe contener al menos un número.")
    return errores

def usuario_existe(nombre_usuario):
    """Verifica si un nombre de usuario ya está registrado."""
    try:
        with open(NOMBRE_ARCHIVO_USUARIOS, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for fila in reader:
                if fila['username'] == nombre_usuario:
                    return True
    except FileNotFoundError:
        return False
    return False

def registrar_nuevo_usuario():
    """Flujo para registrar un nuevo usuario con validación de contraseña."""
    print("\n--- Registro de Nuevo Usuario ---")
    while True:
        nombre_usuario = input("Ingrese un nuevo nombre de usuario: ").strip()
        if not nombre_usuario:
            print("El nombre de usuario no puede estar vacío.")
            continue
        if usuario_existe(nombre_usuario):
            print("Error: El nombre de usuario ya existe. Elija otro.")
            continue
        break

    while True:
        contrasena = input(f"Cree una contraseña para '{nombre_usuario}': ")
        errores = validar_contrasena(contrasena)
        if not errores:
            break
        else:
            print("\n[!] Contraseña no segura:")
            for error in errores:
                print(f"  - {error}")
            print("\nSugerencia: Usa combinaciones de mayúsculas, minúsculas, números y símbolos (>8 caracteres).\n")

    with open(NOMBRE_ARCHIVO_USUARIOS, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([nombre_usuario, contrasena])
    
    print("\n¡Registro exitoso! Accediendo al sistema...")
    menu_principal(nombre_usuario)
    return True

def iniciar_sesion():
    """Flujo para iniciar sesión."""
    print("\n--- Iniciar Sesión ---")
    intentos = 3
    while intentos > 0:
        nombre_usuario = input("Usuario: ").strip()
        contrasena = input("Contraseña: ")
        
        try:
            with open(NOMBRE_ARCHIVO_USUARIOS, mode='r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for fila in reader:
                    if fila['username'] == nombre_usuario and fila['password_simulada'] == contrasena:
                        print("\nAutenticación exitosa.")
                        menu_principal(nombre_usuario)
                        return True
        except FileNotFoundError:
            print("Aún no hay usuarios registrados. Por favor, registre uno.")
            return False

        intentos -= 1
        print(f"\nError: Usuario o contraseña incorrectos. Intentos restantes: {intentos}")
        if intentos > 0:
            if input("¿Reintentar? (s/n): ").lower() != 's':
                return False
    print("Ha excedido el número de intentos.")
    return False

# ==============================================================================
#  SECCIÓN 2: FUNCIONALIDADES PRINCIPALES (Cloud, Conectividad, IA, Análisis)
# ==============================================================================

def get_clima(ciudad):
    """
    [CLOUD/CONECTIVIDAD] Obtiene datos del clima desde la API de OpenWeatherMap.
    """
    if OPENWEATHER_API_KEY == "TU_API_KEY_AQUI_OPENWEATHERMAP":
        print("\n[ERROR] La API key de OpenWeatherMap no está configurada.")
        return None
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={OPENWEATHER_API_KEY}&units=metric&lang=es"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lanza un error para respuestas 4xx/5xx
        return response.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"Error: La ciudad '{ciudad}' no fue encontrada.")
        elif e.response.status_code == 401:
            print("Error: API Key de OpenWeatherMap inválida o no autorizada.")
        else:
            print(f"Error HTTP: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")
    return None

def guardar_en_historial(usuario, ciudad, data):
    """Guarda una consulta de clima en el historial global."""
    fila = [
        usuario,
        ciudad,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        data['main']['temp'],
        data['weather'][0]['description'],
        data['main']['humidity'],
        data['wind']['speed'] * 3.6  # Convertir m/s a km/h
    ]
    with open(NOMBRE_ARCHIVO_HISTORIAL, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(fila)

def consultar_clima_y_guardar(usuario_logueado):
    """Opción 1: Flujo completo para consultar clima y guardar."""
    ciudad = input("\nIngrese el nombre de una ciudad para consultar el clima: ").strip()
    if not ciudad:
        print("El nombre de la ciudad no puede estar vacío.")
        return

    data = get_clima(ciudad)
    if data:
        print("\n--- Clima Actual en " + data['name'] + " ---")
        print(f"  Temperatura: {data['main']['temp']:.1f}°C")
        print(f"  Sensación Térmica: {data['main']['feels_like']:.1f}°C")
        print(f"  Condición: {data['weather'][0]['description'].capitalize()}")
        print(f"  Humedad: {data['main']['humidity']}%")
        print(f"  Viento: {data['wind']['speed']*3.6:.1f} km/h")
        
        guardar_en_historial(usuario_logueado, data['name'], data)
        print("\nConsulta guardada en el historial global.")

def ver_historial_personal(usuario_logueado):
    """Opción 2: Muestra el historial de un usuario para una ciudad."""
    ciudad = input("\nIngrese la ciudad de la cual desea ver su historial: ").strip()
    if not ciudad:
        print("El nombre de la ciudad no puede estar vacío.")
        return

    print(f"\n--- Tu Historial de Consultas para {ciudad} ---")
    encontrado = False
    try:
        with open(NOMBRE_ARCHIVO_HISTORIAL, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader) # Omitir cabecera
            for fila in reader:
                # Formato: [Usuario, Ciudad, Fecha, Temp, Cond, Hum, Viento]
                if fila[0] == usuario_logueado and fila[1].lower() == ciudad.lower():
                    print(f"  - Fecha: {fila[2]}, Temp: {fila[3]}°C, Condición: {fila[4].capitalize()}")
                    encontrado = True
        if not encontrado:
            print("No se encontraron registros para esa ciudad en tu historial.")
    except FileNotFoundError:
        print("El archivo de historial aún no existe. Realiza una consulta primero.")

def mostrar_estadisticas_globales():
    """
    [ANÁLISIS DE DATOS] Opción 3: Calcula y muestra estadísticas del historial global.
    """
    print("\n--- Estadísticas Globales de Uso ---")
    try:
        with open(NOMBRE_ARCHIVO_HISTORIAL, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            cabecera = next(reader)
            datos = list(reader)
            
            if not datos:
                print("El historial está vacío. No se pueden calcular estadísticas.")
                return

            # 1. Número total de consultas
            total_consultas = len(datos)
            print(f"Número total de consultas: {total_consultas}")

            # 2. Ciudad más consultada
            ciudades = [fila[1] for fila in datos]
            ciudad_mas_consultada = Counter(ciudades).most_common(1)[0]
            print(f"Ciudad más consultada: {ciudad_mas_consultada[0]} ({ciudad_mas_consultada[1]} veces)")

            # 3. Temperatura promedio
            temperaturas = [float(fila[3]) for fila in datos]
            temp_promedio = sum(temperaturas) / len(temperaturas)
            print(f"Temperatura promedio registrada: {temp_promedio:.1f}°C")
            
            print("\nEl archivo 'historial_global.csv' está listo para ser usado en Excel o Sheets para crear gráficos.")

    except FileNotFoundError:
        print("El archivo de historial no existe. No hay datos para analizar.")

def obtener_consejo_vestimenta(usuario_logueado):
    """
    [INTELIGENCIA ARTIFICIAL] Opción 4: Usa Gemini para dar consejos de vestimenta.
    """
    if not model:
        print("\n[ERROR] La funcionalidad de IA no está disponible.")
        print("Verifica la configuración de la API Key de Gemini al inicio del script.")
        return

    print("\n--- Consejo IA: ¿Cómo Me Visto Hoy? ---")
    ciudad = input("Ingrese la ciudad para obtener el consejo de vestimenta: ").strip()
    if not ciudad:
        print("El nombre de la ciudad no puede estar vacío.")
        return

    data = get_clima(ciudad)
    if data:
        # Preparamos el prompt para la IA
        temp = data['main']['temp']
        condicion = data['weather'][0]['description']
        humedad = data['main']['humidity']
        viento_kmh = data['wind']['speed'] * 3.6
        
        prompt = f"""
        Actúa como un asistente de moda personal. Basado en el siguiente clima para la ciudad de {ciudad}, 
        dame un consejo breve y práctico sobre qué ropa usar. Sé directo y amigable.

        - Temperatura: {temp:.1f}°C
        - Condición: {condicion}
        - Humedad: {humedad}%
        - Viento: {viento_kmh:.1f} km/h

        Dame el consejo en 2 o 3 frases.
        """
        
        print("\nGenerando consejo con IA... por favor espera.")
        try:
            response = model.generate_content(prompt)
            print("\n--- Consejo de GuardiánClima IA ---")
            print(response.text)
            print("-----------------------------------")
        except Exception as e:
            print(f"\nOcurrió un error al contactar a la IA: {e}")

def mostrar_acerca_de():
    """Opción 5: Muestra información sobre la aplicación y los desarrolladores."""
    print("""
    ==============================================================================
                               GuardiánClima ITBA
    ==============================================================================
    
    Descripción:
    GuardiánClima ITBA es una aplicación de consola educativa diseñada para
    demostrar la integración de conceptos de Programación, Ciberseguridad,
    Análisis de Datos, Inteligencia Artificial y Cloud Computing.
    
    Uso de la Aplicación:
    1. Menú de Acceso: Puedes 'Iniciar Sesión' si ya tienes una cuenta,
       'Registrarte' como nuevo usuario o 'Salir'.
    2. Menú Principal (Post-Login):
       - Consultar Clima: Obtiene el clima actual de una ciudad y lo guarda.
       - Ver Mi Historial: Revisa tus consultas pasadas para una ciudad.
       - Estadísticas Globales: Muestra datos agregados de todas las consultas.
       - Consejo IA: Recibe una recomendación de vestimenta basada en el clima.
       - Acerca De...: Muestra esta información.
       - Cerrar Sesión: Vuelve al Menú de Acceso.
    
    Funcionamiento Interno y Conceptos Aplicados:
    - Ciberseguridad: Durante el registro, tu contraseña es validada para
      asegurar que cumple con criterios de fortaleza (longitud, mayúsculas,
      números).
      ADVERTENCIA: Este es un ejercicio educativo. Las contraseñas se guardan
      en texto plano en 'usuarios_simulados.csv', lo cual es INSEGURO. En una
      aplicación real, se usarían técnicas de hashing y salting para protegerlas.
    - Cloud y Conectividad: Usamos la API de OpenWeatherMap para obtener datos
      climáticos en tiempo real y la API de Google Gemini para la IA.
    - Análisis de Datos: El sistema guarda un 'historial_global.csv' y calcula
      estadísticas como la ciudad más consultada y la temperatura promedio.
    - Inteligencia Artificial: Enviamos los datos del clima a Google Gemini
      para que genere un consejo de vestimenta útil y contextual.
    
    Desarrolladores:
    - José Ignacio Aldaco
    - Joaquín Nicolás Dominguez Gaviola
    - Santiago Ranftl
    - Santiago Ramón Garriga Zimmermann
    - Natan Jonas Rosenhain
    
    ==============================================================================
    """)

# ==============================================================================
#  SECCIÓN 3: MENÚS PRINCIPALES DE LA APLICACIÓN (Flujo de Control)
# ==============================================================================

def menu_principal(usuario_logueado):
    """Muestra el menú principal después del login."""
    print("\n" + "="*40)
    print(f"  ¡Bienvenido(a), {usuario_logueado}!")
    print("  Acceso a GuardiánClima ITBA concedido.")
    print("="*40)
    
    while True:
        print("\n--- Menú Principal ---")
        print("1. Consultar Clima Actual y Guardar en Historial")
        print("2. Ver Mi Historial Personal de Consultas por Ciudad")
        print("3. Estadísticas Globales de Uso")
        print("4. Consejo IA: ¿Cómo Me Visto Hoy?")
        print("5. Acerca De...")
        print("6. Cerrar Sesión")
        
        opcion = input("Seleccione una opción (1-6): ")
        
        if opcion == '1':
            consultar_clima_y_guardar(usuario_logueado)
        elif opcion == '2':
            ver_historial_personal(usuario_logueado)
        elif opcion == '3':
            mostrar_estadisticas_globales()
        elif opcion == '4':
            obtener_consejo_vestimenta(usuario_logueado)
        elif opcion == '5':
            mostrar_acerca_de()
        elif opcion == '6':
            print("\nCerrando sesión...")
            break # Rompe el bucle y vuelve al menú de acceso
        else:
            print("\nOpción no válida. Por favor, elija una opción del 1 al 6.")

def menu_acceso():
    """Muestra el menú de acceso inicial."""
    # Inicialización de archivos
    inicializar_archivo(NOMBRE_ARCHIVO_USUARIOS, ['username', 'password_simulada'])
    inicializar_archivo(NOMBRE_ARCHIVO_HISTORIAL, [
        'NombreDeUsuario', 'Ciudad', 'FechaHora', 'Temperatura_C', 
        'Condicion_Clima', 'Humedad_Porcentaje', 'Viento_kmh'
    ])
    
    print("="*50)
    print("      Bienvenido a GuardiánClima ITBA v1.0")
    print("="*50)
    print("Este es un sistema de simulación con fines educativos.")
    print("[ADVERTENCIA] Las contraseñas se guardan en texto plano.\n")
    
    while True:
        print("\n--- Menú de Acceso ---")
        print("1. Iniciar Sesión")
        print("2. Registrar Nuevo Usuario")
        print("3. Salir de la Aplicación")
        
        opcion = input("Seleccione una opción (1-3): ")
        
        if opcion == '1':
            iniciar_sesion()
        elif opcion == '2':
            registrar_nuevo_usuario()
        elif opcion == '3':
            print("\nGracias por usar GuardiánClima ITBA. ¡Hasta luego!")
            break
        else:
            print("\nOpción no válida. Por favor, elija una opción del 1 al 3.")

# --- Punto de Entrada de la Aplicación ---
if __name__ == "__main__":
    menu_acceso()