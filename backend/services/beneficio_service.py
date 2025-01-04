from models.tarjetaBeneficio import TarjetaBeneficio
from models.reserva import Reserva
from datetime import datetime

def sagarReserva(nroTarjeta, asientos, medioDePago):
    tarjeta = TarjetaBeneficio.obtener_por_nro_tarjeta(nroTarjeta)
    if not tarjeta:
        return {"exito":False, "mensaje":"Tarjeta no encontrada"}
    
    precioInicial = sum(asiento.precio for asiento in asientos)
    descuento = tarjeta.calcular_descuento(precioInicial)
    monto_final = precioInicial - descuento
    
    if not medioDePago.pagar(monto_final):
        return {"exito":False, "mensaje":"Ocurrio un fallo en el pago"}
    
    #no me devuelve nada esto, lo tengo que cambiar
    nuevaReserva = Reserva(datetime.now(), asientos)
    
    return {"exito":True, "mensaje":f"Reserva realizada. Monto final: ${monto_final:.2f}", "reserva": nuevaReserva}
    
