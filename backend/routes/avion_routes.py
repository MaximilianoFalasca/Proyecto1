from flask import Blueprint, jsonify, request
from models import Avion

Avion_routes = Blueprint('avion_routes',__name__)

# aca mas que nada es importante agregar aviones y eliminarlos, tambien modificar los km y demas

@Avion_routes.route('/aviones/<string:matricula>', methods=["GET"])
def obtener_avion(matricula):
    try:
        avion = Avion.obtenerAvion(matricula)
        return jsonify({
            "matricula":avion.matricula,
            "fechaFabricacion":avion.fechaFabricacion,
            "capacidad":avion.capacidad,
            "nombreModelo":avion.nombreModelo,
            "nombreMarca":avion.nombreMarca,
            "kilometros" : avion.kilometros
        }), 200
    except Exception as e:
        return jsonify({"error":str(e)}), 400

@Avion_routes.route('/aviones', methods=['GET'])
def obtener_aviones():
    try:
        aviones = Avion.obtenerTodos()
        return jsonify([
            {
                "matricula":avion.matricula,
                "fechaFabricacion":avion.fechaFabricacion,
                "capacidad":avion.capacidad,
                "nombreModelo":avion.nombreModelo,
                "nombreMarca":avion.nombreMarca,
                "kilometros" : avion.kilometros
            } for avion in aviones
        ]), 200
    except Exception as e:
        return jsonify({"error":str(e)}), 400
    
@Avion_routes.route('/aviones', methods=['POST'])
def registrar_avion():
    avion = request.json
    
    if not avion or not avion.get('matricula') or not avion.get('fechaFabricacion') or not avion.get('capacidad') or not avion.get('nombreModelo') or not avion.get('nombreMarca'):
        return jsonify({"error": "Faltan datos"}), 
    
    try:
        nuevo_avion = Avion(**avion)
        nuevo_avion.guardar()
        return jsonify({"mensaje":"Avion registrado"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400 
    
@Avion_routes.route('/aviones/<string:matricula>', methods=['PUT'])
def modificar_avion(matricula):
    datos = request.json
    try:
        Avion.actualizarAvion(matricula,datos)
        return jsonify({"mensaje":"Datos de avion actualizados con exito"}), 201
    except Exception as e:
        return jsonify({"error":str(e)}), 400
    
@Avion_routes.route('/aviones/<string:matricula>', methods=['DELETE'])
def eliminar_avion(matricula):
    try:
        Avion.eliminarAvion(matricula)
        return jsonify({"mensaje":"Avion eliminado con exito"}), 204
    except Exception as e:
        return jsonify({"error":str(e)}), 400