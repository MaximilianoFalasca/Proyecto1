from flask import Blueprint, jsonify, request
from models import Tripulacion

Tripulacion_routes = Blueprint('tripulacion_routes',__name__)

@Tripulacion_routes.route('/tripulacion/<int:legajo>', methods=["GET"])
def obtener_tripulacion(legajo):
    try:
        tripulacion = Tripulacion.obtenerTripulacion(legajo)
        return jsonify({
            "legajo":tripulacion["legajo"],
            "dni":tripulacion["dni"], 
            "nombre":tripulacion["nombre"], 
            "apellido":tripulacion["apellido"],
            "nroVuelo":tripulacion["nroVuelo"],
            "fechaYHoraSalida":tripulacion["fechaYHoraSalida"],
            "rol":tripulacion["rol"], 
            "numeroTarjeta":tripulacion["numeroTarjeta"],
            "horasAcumuladas" : tripulacion["horasAcumuladas"],
        }), 200
    except Exception as e:
        return jsonify({"error":str(e)}), 400

@Tripulacion_routes.route('/tripulacion', methods=['GET'])
def obtener_tripulaciones():
    try:
        tripulaciones = Tripulacion.obtenerTodos()
        return jsonify([
            {
                "legajo":tripulacion["legajo"],
                "dni":tripulacion["dni"], 
                "nombre":tripulacion["nombre"], 
                "apellido":tripulacion["apellido"],
                "nroVuelo":tripulacion["nroVuelo"],
                "fechaYHoraSalida":tripulacion["fechaYHoraSalida"],
                "rol":tripulacion["rol"], 
                "numeroTarjeta":tripulacion["numeroTarjeta"],
                "horasAcumuladas" : tripulacion["horasAcumuladas"],
            } for tripulacion in tripulaciones
        ]), 200
    except Exception as e:
        return jsonify({"error":str(e)}), 400
    
@Tripulacion_routes.route('/tripulacion', methods=['POST'])
def registrar_tripulacion():
    tripulacion = request.json
    
    if not tripulacion or not tripulacion.get('dni') or not tripulacion.get('cuil') or not tripulacion.get('nombre') or not tripulacion.get('apellido') or not tripulacion.get('nroVuelo') or not tripulacion.get('fechaYHoraSalida') or not tripulacion.get('rol'):
        return jsonify({"error": "Faltan datos"}), 
    
    try:
        nueva_tripulacion = Tripulacion(**tripulacion)
        nueva_tripulacion.guardar()
        return jsonify({"mensaje":"Pasajero registrado"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400 
    
@Tripulacion_routes.route('/tripulacion/<int:legajo>', methods=['PUT'])
def modificar_avion(legajo):
    datos = request.json
    try:
        Tripulacion.actualizarTripulacion(legajo,datos)
        return jsonify({"mensaje":"Datos de pasajero actualizados con exito"}), 201
    except Exception as e:
        return jsonify({"error":str(e)}), 400
    
@Tripulacion_routes.route('/tripulacion/<int:legajo>', methods=['DELETE'])
def eliminar_avion(legajo):
    try:
        Tripulacion.eliminarTripulacion(legajo)
        return jsonify({"mensaje":"Pasajero eliminado con exito"}), 204
    except Exception as e:
        return jsonify({"error":str(e)}), 400