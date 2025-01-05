from flask import Flask
from .models import *
import backend.routes.usuarios as usuarios

def create_app():
    app = Flask(__name__)

    # Inicializar la base de datos
    Usuario.inicializar_bd()

    # Registrar las rutas
    app.register_blueprint(usuarios)

    return app
