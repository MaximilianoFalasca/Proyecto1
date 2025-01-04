from backend import Asiento
import sqlite3

# Asegúrate de que el archivo de base de datos sea el correcto
Asiento.db_path = "backend/database/aerolineasArgentinas.db"  # Cambia a la ruta de tu base de datos si es necesario

# Paso 1: Inicializar la base de datos
print("Inicializando la base de datos...")
Asiento.inicializar_db()

# Paso 2: Crear y guardar un asiento
print("Creando un asiento...")
asiento = Asiento(matricula="ABC123", precio=100)
asiento.guardar()
print(f"Asiento creado con número: {asiento.numero}")

# Paso 3: Verificar que el asiento está en la base de datos
with sqlite3.connect(Asiento.db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM asiento WHERE numero = ?", (asiento.numero,))
    resultado = cursor.fetchone()
    print("Asiento en la base de datos:", resultado)

# Paso 4: Reservar el asiento
print("Reservando el asiento...")
resultado_reserva = asiento.reservar(1)
print("Resultado de la reserva:", resultado_reserva)

# Paso 5: Verificar el estado de la reserva en la base de datos
with sqlite3.connect(Asiento.db_path) as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT numeroReserva FROM asiento WHERE numero = ?", (asiento.numero,))
    resultado = cursor.fetchone()
    print("Reserva en la base de datos:", resultado)

# Paso 6: Intentar reservar el mismo asiento nuevamente
print("Intentando reservar el asiento nuevamente...")
resultado_reserva_duplicada = asiento.reservar(2)
print("Resultado de la reserva duplicada:", resultado_reserva_duplicada)
