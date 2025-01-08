from flask import Blueprint, jsonify, request
from models import Pasajero

Pasajero_routes = Blueprint('routes',__name__)

@Pasajero_routes.route('/pasajeros/<int:dni>', methods=['GET'])
def obtener_pasajero(dni):
    try:
        pasajero = Pasajero.obtenerPasajero(dni)
        return jsonify({
            "dni":pasajero[0], 
            "telefono":pasajero[1], 
            "mail":pasajero[2], 
            "cuil":pasajero[3], 
            "numeroVuelo":pasajero[4], 
            "fechaYHoraSalida":pasajero[5], 
            "nombre":pasajero[6], 
            "apellido":pasajero[7], 
            "numeroTarjeta":pasajero[8]
        }), 200
    except Exception as e:
        return jsonify({"error":str(e)}), 400

@Pasajero_routes.route('/pasajeros', methods=['GET'])
def obtener_pasajeros():
    pasajeros = Pasajero.obtenerTodos()
    return jsonify([
        {
            "dni":pasajero[0], 
            "telefono":pasajero[1], 
            "mail":pasajero[2], 
            "cuil":pasajero[3], 
            "numeroVuelo":pasajero[4], 
            "fechaYHoraSalida":pasajero[5], 
            "nombre":pasajero[6], 
            "apellido":pasajero[7], 
            "numeroTarjeta":pasajero[8]
        } for pasajero in pasajeros
    ]), 200
    
@Pasajero_routes.route('/pasajeros', method=['POST'])
def registrar_pasajero():
    pasajero = request.json
    
    if not pasajero or not pasajero.get('cuil') or not pasajero.get('nombre') or not pasajero.get('apellido') or not pasajero.get('dni') or not pasajero.get('numeroVuelo') or not pasajero.get('fechaYHoraSalida'):
        return jsonify({"error": "Faltan datos"}), 400
    
    try:
        nuevo_pasajero = Pasajero(**pasajero)
        nuevo_pasajero.guardar()
        return jsonify({"mensaje":"Pasajero registrado"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400 
    
@Pasajero_routes.route('/pasajeros/add_card', method=['POST'])
def agregar_tarjeta():
    datos = request.json
    
    if not datos or not datos.get('dni') or not datos.get('numerotarjeta'):
        return jsonify({"error":"Faltan datos"}), 400
    
    try:
        pasajero = Pasajero.obtenerPasajero(datos.get('dni'))
        pasajero.agregarTarjeta(datos.get('numeroTarjeta'))
        return jsonify({"mensaje":"Tarjeta agregada con exito"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@Pasajero_routes.route('/pasajeros/<int:dni>', method=['PUT'])
def modificar_pasajero(dni):
    datos = request.json
    try:
        Pasajero.actualizarPasajero(dni,datos)
        return jsonify({"mensaje":"Datos de pasajero actualizados con exito"}), 201
    except Exception as e:
        return jsonify({"error":str(e)}), 400
    
@Pasajero_routes.route('/pasajeros/<int:dni>', method=['DELETE'])
def eliminar_pasajero(dni):
    try:
        Pasajero.eliminarPasajero(dni)
        return jsonify({"mensaje":"Pasajero eliminado con exito"}), 204
    except Exception as e:
        return jsonify({"error":str(e)}), 400