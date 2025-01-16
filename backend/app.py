from flask import Flask
import sqlite3
from datetime import datetime
from routes import *
from models import * 

# Registrar el adaptador para datetime antes de inicializar la aplicación
sqlite3.register_adapter(datetime, lambda d: d.strftime('%Y-%m-%d %H:%M:%S'))

# Inicializar la base de datos antes de iniciar la aplicación
Asiento.inicializar_db()
Pasajero.inicializar_db()
Persona.inicializar_db()
Reserva.inicializar_bd()
TarjetaBeneficio.inicializar_bd()
Tripulacion.inicializar_db()
Avion.inicializar_db()
Aeropuerto.inicializar_db()
Vuelo.inicializar_db()
       
# Inicializar la aplicación Flask
app = Flask(__name__)

# Registrar el Blueprint
app.register_blueprint(Pasajero_routes)
app.register_blueprint(Avion_routes)
app.register_blueprint(Reserva_routes)
app.register_blueprint(Tripulacion_routes)
app.register_blueprint(Vuelo_routes)
app.register_blueprint(Tarjeta_routes)
app.register_blueprint(Asiento_routes)

if __name__ == '__main__':
    app.run(debug=True)
