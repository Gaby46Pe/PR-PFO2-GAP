from flask import Flask, request, jsonify, render_template
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt_identity
from config import Config
from database import db, User, Task, init_db  # Importamos Task
import os

app = Flask(__name__, template_folder='templates')
app.config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)

# Inicializar la base de datos al inicio
with app.app_context():
    init_db(app)

@app.route('/')
def index():
    return "Servidor Flask de Gestión de Tareas funcionando. Usa los endpoints /registro, /login, /tareas."

# 1. Registro de Usuarios
@app.route('/registro', methods=['POST'])
def registro():
    data = request.get_json()
    if not data or not 'usuario' in data or not 'contraseña' in data:
        return jsonify({"mensaje": "Faltan usuario o contraseña"}), 400

    username = data['usuario']
    password = data['contraseña']

    if User.query.filter_by(username=username).first():
        return jsonify({"mensaje": "El usuario ya existe"}), 409

    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"mensaje": f"Usuario {username} registrado con éxito"}), 201

# 2. Inicio de Sesión
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not 'usuario' in data or not 'contraseña' in data:
        return jsonify({"mensaje": "Faltan usuario o contraseña"}), 400

    username = data['usuario']
    password = data['contraseña']

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"mensaje": "Credenciales inválidas"}), 401

# --- Gestión de Tareas ---

# GET /tareas: Mostrar un HTML de bienvenida (según consigna original)
@app.route('/tareas', methods=['GET'])
@jwt_required()
def welcome_tareas():
    return render_template('welcome.html')

# GET /api/tareas: Listar todas las tareas del usuario logueado
@app.route('/api/tareas', methods=['GET'])
@jwt_required()
def listar_tareas():
    current_username = get_jwt_identity()
    user = User.query.filter_by(username=current_username).first()
    if not user:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404

    tareas = [task.to_dict() for task in user.tasks]
    return jsonify(tareas), 200

# POST /api/tareas: Crear una nueva tarea para el usuario logueado
@app.route('/api/tareas', methods=['POST'])
@jwt_required()
def crear_tarea():
    current_username = get_jwt_identity()
    user = User.query.filter_by(username=current_username).first()
    if not user:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404

    data = request.get_json()
    if not data or not 'title' in data:
        return jsonify({"mensaje": "Falta el título de la tarea"}), 400

    new_task = Task(
        title=data['title'],
        description=data.get('description'),
        user_id=user.id
    )
    db.session.add(new_task)
    db.session.commit()

    return jsonify({"mensaje": "Tarea creada", "tarea": new_task.to_dict()}), 201

# GET /api/tareas/<int:task_id>: Obtener una tarea específica del usuario logueado
@app.route('/api/tareas/<int:task_id>', methods=['GET'])
@jwt_required()
def obtener_tarea(task_id):
    current_username = get_jwt_identity()
    user = User.query.filter_by(username=current_username).first()
    if not user:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404

    task = Task.query.filter_by(id=task_id, user_id=user.id).first()
    if not task:
        return jsonify({"mensaje": "Tarea no encontrada o no pertenece al usuario"}), 404

    return jsonify(task.to_dict()), 200

# PUT /api/tareas/<int:task_id>: Modificar una tarea específica del usuario logueado
@app.route('/api/tareas/<int:task_id>', methods=['PUT'])
@jwt_required()
def modificar_tarea(task_id):
    current_username = get_jwt_identity()
    user = User.query.filter_by(username=current_username).first()
    if not user:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404

    task = Task.query.filter_by(id=task_id, user_id=user.id).first()
    if not task:
        return jsonify({"mensaje": "Tarea no encontrada o no pertenece al usuario"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"mensaje": "No hay datos para actualizar"}), 400

    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.completed = data.get('completed', task.completed)

    db.session.commit()
    return jsonify({"mensaje": "Tarea actualizada", "tarea": task.to_dict()}), 200

# DELETE /api/tareas/<int:task_id>: Eliminar una tarea específica del usuario logueado
@app.route('/api/tareas/<int:task_id>', methods=['DELETE'])
@jwt_required()
def eliminar_tarea(task_id):
    current_username = get_jwt_identity()
    user = User.query.filter_by(username=current_username).first()
    if not user:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404

    task = Task.query.filter_by(id=task_id, user_id=user.id).first()
    if not task:
        return jsonify({"mensaje": "Tarea no encontrada o no pertenece al usuario"}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({"mensaje": "Tarea eliminada"}), 200

if __name__ == '__main__':
    # Para desarrollo, puedes eliminar la base de datos al iniciar (NO en producción)
    # if os.path.exists('tareas.db'):
    #     os.remove('tareas.db')
    #     print("Base de datos eliminada para reinicio.")
    app.run(debug=True)