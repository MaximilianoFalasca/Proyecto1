from flask import Blueprint, jsonify, request
from models import Asiento

Asiento_routes = Blueprint('asiento_routes',__name__)

@Asiento_routes.route('/asientos/<int:numero>/<string:matricula>', methods=["GET"])
def obtener_asiento(numero,matricula):
    try:
        asiento = Asiento.obtenerAsiento(numero,matricula)
        return jsonify({
            "numero":asiento.numero,
            "matricula":asiento.matricula,
            "precio":asiento.precio
        }), 200
    except Exception as e:
        return jsonify({"error":str(e)}), 400

@Asiento_routes.route('/asientos', methods=['GET'])
def obtener_asientos():
    try:
        asientos = Asiento.obtenerTodos()
        return jsonify([
            {
                "numero":asiento.numero,
                "matricula":asiento.matricula,
                "precio":asiento.precio
            } for asiento in asientos
        ]), 200
    except Exception as e:
        return jsonify({"error":str(e)}), 400
    
@Asiento_routes.route('/asientos', methods=['POST'])
def registrar_asiento():
    asiento = request.json
    
    if not asiento or not asiento.get('matricula') or not asiento.get('numero') or not asiento.get('precio'):
        return jsonify({"error": "Faltan datos"}), 
    
    try:
        nuevo_asiento = Asiento(**asiento)
        nuevo_asiento.guardar()
        return jsonify({"mensaje":"Asiento registrado"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400 
    
@Asiento_routes.route('/asientos/<int:numero>/<string:matricula>', methods=['PUT'])
def modificar_asiento(numero,matricula):
    datos = request.json
    try:
        Asiento.actualizarAsiento(numero,matricula,datos)
        return jsonify({"mensaje":"Datos de asiento actualizados con exito"}), 201
    except Exception as e:
        return jsonify({"error":str(e)}), 400
    
@Asiento_routes.route('/asientos/<int:numero>/<string:matricula>', methods=['DELETE'])
def eliminar_asiento(numero,matricula):
    try:
        Asiento.eliminarAsiento(numero,matricula)
        return jsonify({"mensaje":"Asiento eliminado con exito"}), 204
    except Exception as e:
        return jsonify({"error":str(e)}), 400