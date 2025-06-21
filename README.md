# PFO 2: Sistema de Gestión de Tareas con API y Base de Datos

Este proyecto implementa un sistema básico de gestión de tareas con una API REST en Flask y persistencia de datos con SQLite. Incluye registro de usuarios, inicio de sesión con JWT y un endpoint de prueba para tareas.

## Características

* **API REST con Flask:** Endpoints para registro, login y gestión de tareas.
* **Autenticación de Usuarios:** Registro de usuarios con contraseñas hasheadas y login con JSON Web Tokens (JWT).
* **Persistencia de Datos:** Utiliza SQLite para almacenar los usuarios y tareas.
* **Cliente en Consola:** Una aplicación Python para interactuar con la API desde la terminal.

## Requisitos

* Python 3.x
* pip (gestor de paquetes de Python)

## Instalación y Ejecución

Pasos para poner en marcha el proyecto:

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/Gaby46Pe/PR-PFO2-GAP.git
    cd pfo2-tareas
    ```

2.  **Crear y activar el entorno virtual:**
    ```bash
    python -m venv venv
    # En Windows:
    .\venv\Scripts\activate
    # En Linux/macOS:
    source venv/bin/activate
    ```

3.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```
    (Si no tiene `requirements.txt`, ejecutar `pip install Flask Flask-SQLAlchemy Werkzeug Flask-JWT-Extended requests` y luego `pip freeze > requirements.txt`).

4.  **Ejecutar el Servidor Flask:**
    Abrir una terminal, activar el entorno virtual (si no se hizo) y ejecutar:
    ```bash
    python servidor.py
    ```
    El servidor se iniciará en `http://127.0.0.1:5000`. Se verá un archivo `tareas.db` aparecer en el directorio del proyecto.

5.  **Ejecutar el Cliente en Consola:**
    Abrir **otra terminal diferente**, activar el entorno virtual y ejecutar:
    ```bash
    python cliente.py
    ```
    Seguir el menú para registrar un usuario, iniciar sesión y acceder a las tareas.

## Menú del Cliente en Consola

Al ejecutar `python cliente.py` verás un menú interactivo en la terminal:

```
--- Cliente de Gestión de Tareas ---
1. Registrar Usuario
2. Iniciar Sesión
3. Bienvenida
4. Crear Tarea
5. Modificar Tarea
6. Eliminar Tarea
7. Listar Tareas
8. Cerrar Sesión
9. Salir
Elige una opción:
```

- **Registrar Usuario:** Crea un nuevo usuario.
- **Iniciar Sesión:** Inicia sesión y obtiene el token JWT.
- **Bienvenida:** Muestra el HTML de bienvenida (requiere login).
- **Crear Tarea:** Permite crear una tarea nueva.
- **Modificar Tarea:** Permite editar título, descripción y marcar como completada (`1=Sí`, `2=No`).
- **Eliminar Tarea:** Elimina una tarea por ID.
- **Listar Tareas:** Muestra todas las tareas del usuario autenticado.
- **Cerrar Sesión:** Elimina el token de autenticación del cliente.
- **Salir:** Cierra el cliente.

## Endpoints de la API

* **`POST /registro`**
    * **Descripción:** Registra un nuevo usuario en el sistema.
    * **Request Body (JSON):**
        ```json
        {
            "usuario": "nombre_de_usuario",
            "contraseña": "contraseña_segura"
        }
        ```
    * **Respuestas:**
        * `201 Created`: `{"mensaje": "Usuario <nombre> registrado con éxito"}`
        * `400 Bad Request`: `{"mensaje": "Faltan usuario o contraseña"}`
        * `409 Conflict`: `{"mensaje": "El usuario ya existe"}`

* **`POST /login`**
    * **Descripción:** Autentica a un usuario y devuelve un token JWT.
    * **Request Body (JSON):**
        ```json
        {
            "usuario": "nombre_de_usuario",
            "contraseña": "contraseña_del_usuario"
        }
        ```
    * **Respuestas:**
        * `200 OK`: `{"access_token": "..."}`
        * `400 Bad Request`: `{"mensaje": "Faltan usuario o contraseña"}`
        * `401 Unauthorized`: `{"mensaje": "Credenciales inválidas"}`

* **`GET /tareas`**
    * **Descripción:** Muestra un HTML de bienvenida. Requiere autenticación JWT.
    * **Headers:** `Authorization: Bearer <access_token>`
    * **Respuestas:**
        * `200 OK`: Contenido HTML de la página de bienvenida.
        * `401 Unauthorized`: Si el token no es válido o está ausente.

* **`GET /api/tareas`**
    * **Descripción:** Lista todas las tareas del usuario autenticado (respuesta en JSON).
    * **Headers:** `Authorization: Bearer <access_token>`

* **`POST /api/tareas`**
    * **Descripción:** Crea una nueva tarea para el usuario autenticado.
    * **Headers:** `Authorization: Bearer <access_token>`
    * **Request Body (JSON):**
        ```json
        {
            "title": "Título de la tarea",
            "description": "Descripción opcional"
        }
        ```

* **`PUT /api/tareas/<id>`**
    * **Descripción:** Modifica una tarea existente (título, descripción, completada).
    * **Headers:** `Authorization: Bearer <access_token>`
    * **Request Body (JSON):**
        ```json
        {
            "title": "Nuevo título",
            "description": "Nueva descripción",
            "completed": true
        }
        ```

* **`DELETE /api/tareas/<id>`**
    * **Descripción:** Elimina una tarea por ID.
    * **Headers:** `Authorization: Bearer <access_token>`

## Capturas de Pantalla de Pruebas Exitosas

**(Aquí deberás insertar tus capturas de pantalla, por ejemplo):**
* Registro de un usuario exitoso (salida del cliente y/o POSTMAN).
* Inicio de sesión exitoso y obtención del token (salida del cliente y/o POSTMAN).
* Acceso al endpoint `/tareas` con el token (salida del cliente mostrando HTML o captura del navegador).
* Intento de acceso a `/tareas` sin token (salida del cliente mostrando error 401).
* Creación, modificación, eliminación y listado de tareas desde el cliente en consola.

## Alojamiento en GitHub Pages

GitHub Pages es para sitios web estáticos (HTML, CSS, JavaScript). Esta API es dinámica y requiere un servidor Python en ejecución. Por lo tanto, no se puede "alojar" la API directamente en GitHub Pages. Sin embargo, **la documentación (este README.md)** se puede visualizar elegantemente a través de GitHub Pages.

Para ver esta documentación como una página web:
1.  Asegúrate de que tu repositorio sea público.
2.  Ve a la pestaña "Settings" de tu repositorio en GitHub.
3.  Haz clic en "Pages" en la barra lateral izquierda.
4.  En "Build and deployment", selecciona "Deploy from a branch" y luego la rama `main` (o la que uses) y la carpeta `/ (root)`.
5.  Guarda los cambios. GitHub Pages generará una URL (ej. `https://<tu-usuario>.github.io/<nombre-del-repositorio>/`) donde podrás ver este `README.md` renderizado.

---