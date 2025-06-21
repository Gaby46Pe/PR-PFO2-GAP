import requests
import json

BASE_URL = "http://127.0.0.1:5000"
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
            print("Token de acceso obtenido. (No se muestra completo por seguridad)")
        print("Respuesta:", response.json())
    except requests.exceptions.ConnectionError:
        print("Error: No se pudo conectar al servidor. Asegúrate de que el servidor Flask esté corriendo.")

def cerrar_sesion():
    global AUTH_TOKEN
    AUTH_TOKEN = None
    print("\nSesión cerrada correctamente.")

def obtener_tareas_html():
    print("\n--- Obteniendo HTML de bienvenida de tareas ---")
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
        if response.status_code == 200:
            print("Contenido HTML recibido (primeras 200 caracteres):")
            print(response.text[:200])
        else:
            print("Respuesta (JSON si es error):", response.json())
    except requests.exceptions.ConnectionError:
        print("Error: No se pudo conectar al servidor. Asegúrate de que el servidor Flask esté corriendo.")

def listar_tareas_json():
    print("\n--- Listando tareas (JSON) ---")
    url = f"{BASE_URL}/api/tareas"
    headers = {'Content-Type': 'application/json'}
    if AUTH_TOKEN:
        headers['Authorization'] = f'Bearer {AUTH_TOKEN}'
    else:
        print("Advertencia: No hay token de autenticación. Inicia sesión primero.")
        return

    try:
        response = requests.get(url, headers=headers)
        print("Estado:", response.status_code)
        print("Respuesta:", json.dumps(response.json(), indent=2))
    except requests.exceptions.ConnectionError:
        print("Error: No se pudo conectar al servidor. Asegúrate de que el servidor Flask esté corriendo.")
    except json.JSONDecodeError:
        print("Error al decodificar JSON. Posiblemente la respuesta no es JSON.")
        print("Respuesta completa:", response.text)

def crear_tarea(title, description=None):
    print(f"\n--- Creando tarea: {title} ---")
    url = f"{BASE_URL}/api/tareas"
    headers = {'Content-Type': 'application/json'}
    if AUTH_TOKEN:
        headers['Authorization'] = f'Bearer {AUTH_TOKEN}'
    else:
        print("Advertencia: No hay token de autenticación. Inicia sesión primero.")
        return

    data = {"title": title}
    if description:
        data["description"] = description

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        print("Estado:", response.status_code)
        print("Respuesta:", json.dumps(response.json(), indent=2))
    except requests.exceptions.ConnectionError:
        print("Error: No se pudo conectar al servidor. Asegúrate de que el servidor Flask esté corriendo.")
    except json.JSONDecodeError:
        print("Error al decodificar JSON. Posiblemente la respuesta no es JSON.")
        print("Respuesta completa:", response.text)

def modificar_tarea(task_id, title=None, description=None, completed=None):
    print(f"\n--- Modificando tarea ID: {task_id} ---")
    url = f"{BASE_URL}/api/tareas/{task_id}"
    headers = {'Content-Type': 'application/json'}
    if AUTH_TOKEN:
        headers['Authorization'] = f'Bearer {AUTH_TOKEN}'
    else:
        print("Advertencia: No hay token de autenticación. Inicia sesión primero.")
        return

    data = {}
    if title is not None:
        data['title'] = title
    if description is not None:
        data['description'] = description
    if completed is not None:
        data['completed'] = completed

    if not data:
        print("No hay datos para actualizar.")
        return

    try:
        response = requests.put(url, headers=headers, data=json.dumps(data))
        print("Estado:", response.status_code)
        print("Respuesta:", json.dumps(response.json(), indent=2))
    except requests.exceptions.ConnectionError:
        print("Error: No se pudo conectar al servidor. Asegúrate de que el servidor Flask esté corriendo.")
    except json.JSONDecodeError:
        print("Error al decodificar JSON. Posiblemente la respuesta no es JSON.")
        print("Respuesta completa:", response.text)

def eliminar_tarea(task_id):
    print(f"\n--- Eliminando tarea ID: {task_id} ---")
    url = f"{BASE_URL}/api/tareas/{task_id}"
    headers = {'Content-Type': 'application/json'}
    if AUTH_TOKEN:
        headers['Authorization'] = f'Bearer {AUTH_TOKEN}'
    else:
        print("Advertencia: No hay token de autenticación. Inicia sesión primero.")
        return

    try:
        response = requests.delete(url, headers=headers)
        print("Estado:", response.status_code)
        if response.status_code == 200:
            print("Respuesta:", json.dumps(response.json(), indent=2))
        else:
            print("Respuesta:", response.text)
    except requests.exceptions.ConnectionError:
        print("Error: No se pudo conectar al servidor. Asegúrate de que el servidor Flask esté corriendo.")
    except json.JSONDecodeError:
        print("Error al decodificar JSON. Posiblemente la respuesta no es JSON.")
        print("Respuesta completa:", response.text)

def mostrar_menu():
    print("\n--- Cliente de Gestión de Tareas ---")
    print("1. Registrar Usuario")
    print("2. Iniciar Sesión")
    print("3. Bienvenida")
    print("4. Crear Tarea")
    print("5. Modificar Tarea")
    print("6. Eliminar Tarea")
    print("7. Listar Tareas")
    print("8. Cerrar Sesión")
    print("9. Salir")
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
            obtener_tareas_html()
        elif choice == '4':
            title = input("Título de la tarea: ")
            desc = input("Descripción (opcional): ")
            crear_tarea(title, desc if desc else None)
        elif choice == '5':
            try:
                task_id = int(input("ID de la tarea a modificar: "))
                title = input("Nuevo título (dejar vacío para no cambiar): ")
                desc = input("Nueva descripción (dejar vacío para no cambiar): ")
                completed_str = input("¿Tarea completada? (1=Sí, 2=No, dejar vacío para no cambiar): ").strip()
                completed = None
                if completed_str == '1':
                    completed = True
                elif completed_str == '2':
                    completed = False

                modificar_tarea(
                    task_id,
                    title if title else None,
                    desc if desc else None,
                    completed
                )
            except ValueError:
                print("ID de tarea inválido.")
        elif choice == '6':
            try:
                task_id = int(input("ID de la tarea a eliminar: "))
                eliminar_tarea(task_id)
            except ValueError:
                print("ID de tarea inválido.")
        elif choice == '7':
            listar_tareas_json()
        elif choice == '8':
            cerrar_sesion()
        elif choice == '9':
            print("Saliendo...")
            break
        else:
            print("Opción inválida. Inténtalo de nuevo.")