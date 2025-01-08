from flask import Blueprint, jsonify, request
from models import Reserva

Pasajero_routes = Blueprint('routes',__name__)
asdasdaisdbvais.asdansp
@Pasajero_routes.routasdasde(a'/reservas/<int:nro>/<string:fecha>', methods=['GET'])
def obtener_vuelo(nro, fecha):
    try:
        # Convertir la fecha a formato datetime
        from datetime import datetime
        fecha_salida = datetime.strptime(fecha, '%Y-%m-%d').date()
        
        # Llamar al método del modelo para obtener el vuelo
        vuelo = Vuelo.obtenerVuelo(nro, fecha_salida)
        
        return jsonify({
            "nro" : vuelo[0],
            "fechaYHoraSalida" : vuelo[1],
            "fechaYHoraLlegada" : vuelo[2],
            "matricula" : vuelo[3],
            "codigoAeropuertoSalida" : vuelo[4],
            "codigoAeropuertoLlegada" : vuelo[5],
        }), 200
    except Exception as e:
        return jsonify({"error":str(e)}), 400

@Pasajero_routes.route('/vuelos', methods=['GET'])
def obtener_vuelos():
    vuelos = Vuelo.obtenerTodos()
    return jsonify([
        {
            "nro" : vuelo[0],
            "fechaYHoraSalida" : vuelo[1],
            "fechaYHoraLlegada" : vuelo[2],
            "matricula" : vuelo[3],
            "codigoAeropuertoSalida" : vuelo[4],
            "codigoAeropuertoLlegada" : vuelo[5],
        } for vuelo in vuelos
    ])
    
@Pasajero_routes.route('/vuelos', method=['POST'])
def registrar_vuelo():
    vuelo = request.json
    
    if not vuelo or not vuelo.get('nro') or not vuelo.get('fechaYHoraSalida') or not vuelo.get('matricula') or not vuelo.get('codigoAeropuertoSalida') or not vuelo.get('codigoAeropuertoLlegada'):
        return jsonify({"error": "Faltan datos"}), 400
    
    try:
        nuevo_vuelo = Vuelo(**vuelo)
        nuevo_vuelo.guardar()
        return jsonify({"mensaje":"Vuelo registrado"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400 

@Pasajero_routes.route('/vuelos/<int:nro>/<string:fecha>', method=['PUT'])
def finalizar_vuelo(nro,fecha):
    try:
        vuelo = Vuelo.obtenerVuelo(nro,fecha)
        vuelo.finalizarVuelo()
        return jsonify({"mensaje":"Vuelo finalizado con exito"}), 201
    except Exception as e:
        return jsonify({"error":str(e)}), 400
    
@Pasajero_routes.route('/vuelos/<int:nro>/<string:fecha>', method=['DELETE'])
def eliminar_vuelo(nro,fecha):
    try:
        Vuelo.eliminarVuelo(nro,fecha)
        return jsonify({"mensaje":"Vuelo eliminado con exito"}), 204
    except Exception as e:
        return jsonify({"error":str(e)}), 400