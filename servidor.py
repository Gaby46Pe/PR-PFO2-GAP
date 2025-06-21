from flask import Flask, request, jsonify, render_template
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt_identity
from config import Config
from database import db, User, init_db
import os

app = Flask(__name__, template_folder='templates') # Especificar la carpeta de templates
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
        return jsonify({"mensaje": "El usuario ya existe"}), 409 # Conflict

    new_user = User(username=username)
    new_user.set_password(password) # Hashear y guardar contraseña
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"mensaje": f"Usuario {username} registrado con éxito"}), 201 # Created

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
        return jsonify({"mensaje": "Credenciales inválidas"}), 401 # Unauthorized

# 3. Gestión de Tareas (Endpoint protegido)
@app.route('/tareas', methods=['GET', 'POST'])
@jwt_required() # Protege este endpoint, requiere un JWT válido
def crear_tarea():
    data = request.get_json()
    if not data or not data.get('titulo'):
        return jsonify({"mensaje": "Falta el título de la tarea"}), 400
    nueva_tarea = Tarea(titulo=data['titulo'], usuario_id=get_jwt_identity())
    db.session.add(nueva_tarea)
    db.session.commit()
    return jsonify({"mensaje": "Tarea creada"}), 201

def tareas():
    current_user = get_jwt_identity() # Obtiene la identidad del token JWT
    # En un proyecto real, aquí iría la lógica para listar o gestionar tareas.
    # Por ahora, solo devuelve el HTML de bienvenida.
    return render_template('welcome.html')

if __name__ == '__main__':
    # Puedes configurar el puerto aquí, por ejemplo, app.run(debug=True, port=5000)
    app.run(debug=True) # debug=True para desarrollo (recarga automática)