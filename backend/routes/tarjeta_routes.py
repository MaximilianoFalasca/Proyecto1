from flask import Blueprint, jsonify, request
from models import TarjetaBeneficio

Tarjeta_routes = Blueprint('tarjeta_routes',__name__)

# aca mas que nada es importante agregar aviones y eliminarlos, tambien modificar los km y demas

@Tarjeta_routes.route('/tarjetas/<string:nroTarjeta>', methods=["GET"])
def obtener_tarjeta(nroTarjeta):
    try:
        tarjeta = TarjetaBeneficio.obtener_por_nro_tarjeta(nroTarjeta)
        return jsonify({
            "numero":tarjeta.nroTarjeta,
            "puntos":tarjeta.puntos
        }), 200
    except Exception as e:
        return jsonify({"error":str(e)}), 400

@Tarjeta_routes.route('/tarjetas', methods=['GET'])
def obtener_tarjetas():
    try:
        tarjetas = TarjetaBeneficio.obtenerTodos()
        return jsonify([
            {
                "numero":tarjeta.nroTarjeta,
                "puntos":tarjeta.puntos
            } for tarjeta in tarjetas
        ]), 200
    except Exception as e:
        return jsonify({"error":str(e)}), 400
    
@Tarjeta_routes.route('/tarjetas', methods=['POST'])
def registrar_tarjeta():
    tarjeta = request.json
    
    if not tarjeta or not tarjeta.get('nroTarjeta'):
        return jsonify({"error": "Faltan datos"}), 
    
    try:
        nuevo_avion = TarjetaBeneficio(**tarjeta)
        nuevo_avion.guardar()
        return jsonify({"mensaje":"Tarjeta registrado"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400 
    
@Tarjeta_routes.route('/tarjetas/<string:nroTarjeta>', methods=['PUT'])
def modificar_tarjeta(nroTarjeta):
    data = request.json
    puntos = data.get('puntos')
    
    try:
        TarjetaBeneficio.actualizarTarjeta(nroTarjeta,puntos)
        return jsonify({"mensaje":"Datos de tarjeta actualizados con exito"}), 201
    except Exception as e:
        return jsonify({"error":str(e)}), 400
    
@Tarjeta_routes.route('/tarjetas/<string:nroTarjeta>', methods=['DELETE'])
def eliminar_tarjeta(nroTarjeta):
    try:
        TarjetaBeneficio.eliminarTarjeta(nroTarjeta)
        return jsonify({"mensaje":"Tarjeta eliminada con exito"}), 204
    except Exception as e:
        return jsonify({"error":str(e)}), 400