import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'una-cadena-secreta-muy-segura-y-dificil-de-adivinar'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tareas.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'otra-clave-secreta-para-jwt' # Clave para JWT