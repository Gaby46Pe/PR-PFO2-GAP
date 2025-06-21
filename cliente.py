import requests
import json

BASE_URL = "http://127.0.0.1:5000"  # Asegúrate de que coincida con el puerto de tu servidor Flask
AUTH_TOKEN = None

def registrar_usuario(usuario, password):
    print(f"\n--- Registrando usuario: {usuario} ---")
    url = f"{BASE_URL}/registro"
    headers = {'Content-Type': 'application/json'}
    data = {"usuario": usuario, "contraseña": password}
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print("Estado:", response.status_code)
        print("Respuesta:", response.json())
    except requests.exceptions.ConnectionError:
        print("Error: No se pudo conectar al servidor. Asegúrate de que el servidor Flask esté corriendo.")

def iniciar_sesion(usuario, password):
    global AUTH_TOKEN
    print(f"\n--- Iniciando sesión para: {usuario} ---")
    url = f"{BASE_URL}/login"
    headers = {'Content-Type': 'application/json'}
    data = {"usuario": usuario, "contraseña": password}
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print("Estado:", response.status_code)
        if response.status_code == 200:
            AUTH_TOKEN = response.json().get('access_token')
            print("Token de acceso obtenido:", AUTH_TOKEN)
        print("Respuesta:", response.json())
    except requests.exceptions.ConnectionError:
        print("Error: No se pudo conectar al servidor. Asegúrate de que el servidor Flask esté corriendo.")

def obtener_tareas():
    print("\n--- Obteniendo tareas ---")
    url = f"{BASE_URL}/tareas"
    headers = {'Content-Type': 'application/json'}
    if AUTH_TOKEN:
        headers['Authorization'] = f'Bearer {AUTH_TOKEN}'
    else:
        print("Advertencia: No hay token de autenticación. Inicia sesión primero.")
        return

    try:
        response = requests.get(url, headers=headers)
        print("Estado:", response.status_code)
        # Para el endpoint /tareas, esperamos HTML, no JSON
        if response.status_code == 200:
            print("Contenido HTML recibido (primeras 200 caracteres):")
            print(response.text[:200]) # Imprimir solo una parte del HTML
        else:
            print("Respuesta (JSON si es error):", response.json())
    except requests.exceptions.ConnectionError:
        print("Error: No se pudo conectar al servidor. Asegúrate de que el servidor Flask esté corriendo.")

def mostrar_menu():
    print("\n--- Cliente de Gestión de Tareas ---")
    print("1. Registrar Usuario")
    print("2. Iniciar Sesión")
    print("3. Obtener Tareas (Requiere Login)")
    print("4. Salir")
    choice = input("Elige una opción: ")
    return choice

if __name__ == '__main__':
    while True:
        choice = mostrar_menu()
        if choice == '1':
            user = input("Usuario: ")
            pwd = input("Contraseña: ")
            registrar_usuario(user, pwd)
        elif choice == '2':
            user = input("Usuario: ")
            pwd = input("Contraseña: ")
            iniciar_sesion(user, pwd)
        elif choice == '3':
            obtener_tareas()
        elif choice == '4':
            print("Saliendo...")
            break
        else:
            print("Opción inválida. Inténtalo de nuevo.")