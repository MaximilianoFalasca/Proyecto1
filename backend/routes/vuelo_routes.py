from flask import Blueprint, jsonify, request
from models import Vuelo

Vuelo_routes = Blueprint('vuelo_routes',__name__)

@Vuelo_routes.route('/vuelos/<int:nro>/<string:fechaSalida>', methods=['GET'])
def obtener_vuelo(nro, fechaSalida):
    try:
        # Convertir la fecha a formato datetime
        from datetime import datetime
        fecha_hora = datetime.strptime(fechaSalida, "%Y-%m-%dT%H:%M:%S")
        
        # Llamar al método del modelo para obtener el vuelo
        vuelo = Vuelo.obtenerVuelo(nro, fecha_hora)
        
        return jsonify({
            "nro" : vuelo.nro,
            "fechaYHoraSalida" : vuelo.fechaYHoraSalida,
            "fechaYHoraLlegada" : vuelo.fechaYHoraLlegada,
            "matricula" : vuelo.matricula,
            "codigoAeropuertoSalida" : vuelo.codigoAeropuertoSalida,
            "codigoAeropuertoLlegada" : vuelo.codigoAeropuertoLlegada,
        }), 200
    except Exception as e:
        return jsonify({"error":str(e)}), 400

@Vuelo_routes.route('/vuelos', methods=['GET'])
def obtener_vuelos():
    vuelos = Vuelo.obtenerTodos()
    return jsonify([
        {
            "nro" : vuelo.nro,
            "fechaYHoraSalida" : vuelo.fechaYHoraSalida,
            "fechaYHoraLlegada" : vuelo.fechaYHoraLlegada,
            "matricula" : vuelo.matricula,
            "codigoAeropuertoSalida" : vuelo.codigoAeropuertoSalida,
            "codigoAeropuertoLlegada" : vuelo.codigoAeropuertoLlegada,
        } for vuelo in vuelos
    ])
    
@Vuelo_routes.route('/vuelos', methods=['POST'])
def registrar_vuelo():
    vuelo = request.json
    
    if not vuelo or not vuelo.get('nro') or not vuelo.get('fechaYHoraSalida') or not vuelo.get('fechaYHoraLlegada') or not vuelo.get('matricula') or not vuelo.get('codigoAeropuertoSalida') or not vuelo.get('codigoAeropuertoLlegada'):
        return jsonify({"error": "Faltan datos"}), 400
    
    try:
        nuevo_vuelo = Vuelo(**vuelo)
        nuevo_vuelo.guardar()
        return jsonify({"mensaje":"Vuelo registrado"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400 

@Vuelo_routes.route('/vuelos/<int:nro>/<string:fechaSalida>', methods=['PUT'])
def finalizar_vuelo(nro,fechaSalida):
    try:
        from datetime import datetime
        
        fecha= datetime.strptime(fechaSalida,'%Y-%m-%dT%H:%M:%S')
        
        vuelo = Vuelo.obtenerVuelo(nro,fecha)
        vuelo.finalizarVuelo()
        return jsonify({"mensaje":"Vuelo finalizado con exito"}), 201
    except Exception as e:
        return jsonify({"error":str(e)}), 400
    
@Vuelo_routes.route('/vuelos/<int:nro>/<string:fechaSalida>', methods=['DELETE'])
def eliminar_vuelo(nro,fechaSalida):
    try:
        from datetime import datetime
        
        fecha = datetime.strptime(fechaSalida, '%Y-%m-%dT%H:%M:%S')
        
        Vuelo.eliminarVuelo(nro,fecha)
        return jsonify({"mensaje":"Vuelo eliminado con exito"}), 204
    except Exception as e:
        return jsonify({"error":str(e)}), 400