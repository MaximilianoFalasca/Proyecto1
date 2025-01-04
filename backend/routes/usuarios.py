from flask import Blueprint, jsonify, request
from backend.models.usuario import Usuario
import sqlite3

Usuarios_routes = Blueprint('routes', __name__)

@Usuarios_routes.route('/api/usuarios', methods=['GET'])
def obtener_usuarios():
    usuarios = Usuario.obtener_todos()
    return jsonify([{"id": u.id, "nombre": u.nombre, "email": u.email} for u in usuarios])

@Usuarios_routes.route('/api/usuarios', methods=['POST'])
def registrar_usuario():
    datos = request.json
    if not datos or not datos.get('nombre') or not datos.get('email'):
        return jsonify({"error": "Faltan datos"}), 400

    try:
        nuevo_usuario = Usuario(nombre=datos['nombre'], email=datos['email'])
        nuevo_usuario.guardar()
        return jsonify({"mensaje": "Usuario registrado", "id": nuevo_usuario.id}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "El email ya está registrado"}), 409
