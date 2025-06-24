# PFO 2: Sistema de Gestión de Tareas con API y Base de Datos

Este proyecto implementa un sistema básico de gestión de tareas con una API REST en Flask y persistencia de datos con SQLite. Incluye registro de usuarios, inicio de sesión con JWT y un endpoint de prueba para tareas.

## Características

* **API REST con Flask:** Endpoints para registro, login y gestión de tareas.
* **Autenticación de Usuarios:** Registro de usuarios con contraseñas hasheadas y login con JSON Web Tokens (JWT).
* **Persistencia de Datos:** Utiliza SQLite para almacenar los usuarios y tareas.
* **Cliente en Consola:** Una aplicación Python para interactuar con la API desde la terminal.

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

  