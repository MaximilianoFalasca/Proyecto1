from flask import Blueprint, jsonify, request
from models import Reserva

Reserva_routes = Blueprint('reserva_routes',__name__)

@Reserva_routes.route('/reservas/<int:numero>', methods=['GET'])
def obtener_reserva(numero):
    try:
        # Llamar al método del modelo para obtener el vuelo
        reserva = Reserva.obtenerReserva(numero)
        
        return jsonify({
            "numero" : reserva.numero,
            "fecha" : reserva.fecha,
            "estado" : reserva.estado,
            "asientos": [
                {"numero": asiento.numero, "matricula": asiento.matricula, "precio": asiento.precio}
                for asiento in reserva.asientos
            ],
            "Pasajero":reserva.dni,
        }), 200
    except Exception as e:
        return jsonify({"error":str(e)}), 400

@Reserva_routes.route('/reservas', methods=['GET'])
def obtener_reservas():
    try:
        reservas = Reserva.obtenerTodos()
        
        return jsonify([
            {
                "numero" : reserva.numero,
                "fecha" : reserva.fecha,
                "estado" : reserva.estado,
                "asientos": [
                    {"numero": asiento.numero, "matricula": asiento.matricula, "precio": asiento.precio}
                    for asiento in reserva.asientos
                ],
                "Pasajero":reserva.dni,
            } for reserva in reservas
        ])
    except Exception as e:
        return jsonify({"error":str(e)}), 400
    
@Reserva_routes.route('/reservas', methods=['POST'])
def registrar_reserva():
    from models import Asiento, Persona, Vuelo
    datos_reserva = request.json
    
    if not datos_reserva or not datos_reserva["dni"] or not datos_reserva["vuelo"] or not datos_reserva["asientos"]:
        return jsonify({"error": "Faltan datos"})
    
    if not all(d in datos_reserva["vuelo"] for d in ["nro", "fechaYHoraSalida"]):
        return jsonify({"error": "Para obtener un vuelo en especifico hace falta que se envie el numero y la fecha y hora de salida"})
    
    try:
        datos_asientos = datos_reserva.pop("asientos",[])
        asientos = []
        # verificamos que tengan los datos necesarios para buscarlos y obtenemos sus instancias
        for asiento in datos_asientos:
            if not all(a in asiento for a in ["matricula", "numero"]):
                return jsonify({"error": "Datos de asiento incompletos"}), 400
            asientos.append(Asiento.obtenerAsiento(asiento["numero"],asiento["matricula"]))
            
        persona = Persona.obtenerPersona(datos_reserva["dni"])
        
        vuelo = Vuelo.obtenerVuelo(datos_reserva["vuelo"]["nro"], datos_reserva["vuelo"]["fechaYHoraSalida"])
        vuelo.toString()
        
        nueva_reserva = persona.sacarReserva(vuelo ,asientos)
        
        return jsonify({
            "message": "Reserva creada exitosamente",
            "reserva": {
                "numero": nueva_reserva.numero,
                "fecha": nueva_reserva.fecha,
                "estado": nueva_reserva.estado,
                "asientos": [
                    {"numero": asiento.numero, "matricula": asiento.matricula, "precio": asiento.precio}
                    for asiento in nueva_reserva.asientos
                ],
                "Pasajero": nueva_reserva.dni,
            }
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 400 

@Reserva_routes.route('/reservas/<int:numero>/asientos', methods=['PUT'])
def cambiar_asientos(numero):
    from models import Asiento
    try:
        datos_asientos = request.json
        asientos = []
        for asiento in datos_asientos["asientos"]:
            if not all (a in asiento for a in ["numero","matricula"]):
                return jsonify({"error": "Datos de asiento incompletos"}), 400  
            asientos.append(Asiento.obtenerAsiento(asiento["numero"],asiento["matricula"]))   
        
        reserva = Reserva.obtenerReserva(numero)
        
        reserva.cambiarAsientos(asientos)
        
        return jsonify({"mensaje":"Asientos cambiados con exito"}), 201
    except Exception as e:
        return jsonify({"error":str(e)}), 400
    

@Reserva_routes.route('/reservas/<int:numero>', methods=['PUT'])
def cambiar_Estado(numero):
    from models.estados import validarEstado
    try:
        estado = request.json
        
        if not estado or not estado["estado"]:
            return jsonify({"error":"se debe enviar un estado"})
        
        if not validarEstado(estado["estado"]):
            return jsonify({"error":"El estado ingresado no es valido"})
        
        reserva = Reserva.obtenerReserva(numero)
        
        reserva.cambiarEstado(estado["estado"])
        
        return jsonify({"mensaje":"Estado cambiado con exito"}), 201
    except Exception as e:
        return jsonify({"error":str(e)}), 400
    
@Reserva_routes.route('/reservas/<int:numero>', methods=['DELETE'])
def eliminar_reserva(numero):
    try:
        reserva = Reserva.obtenerReserva(numero)
        
        if reserva.estado == 'Cancelled':
            Reserva.eliminarReserva(numero)
            return jsonify({"message": f"Reserva {numero} eliminada con éxito"}), 200
        else:
            return jsonify({"error": "Solo se pueden eliminar reservas canceladas"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400
