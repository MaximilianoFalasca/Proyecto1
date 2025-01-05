import sqlite3
import os

class Asiento:
    db_path = "C:/Users/maxi/Desktop/python/Proyecto1/backend/database/aerolineasArgentinas.db"
    
    @classmethod
    def inicializar_db(cls):
        with sqlite3.connect(cls.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS asiento")  # Elimina la tabla si existe
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS asiento(
                    numero INTEGER PRIMARY KEY AUTOINCREMENT,
                    numeroReserva INTEGER,
                    matricula TEXT NOT NULL,
                    precio REAL NOT NULL,
                    FOREIGN KEY (numeroReserva) REFERENCES reserva(numero),
                    FOREIGN KEY (matricula) REFERENCES avion(matricula)
                )               
            """)
            conn.commit()
    
    def __init__(self, matricula, precio, numeroReserva=None):
        self.numeroReserva = numeroReserva
        self.matricula = matricula
        self.precio = precio
    
    def guardar(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO asiento (numeroReserva, matricula, precio) VALUES (?,?,?)",(self.numeroReserva,self.matricula,self.precio))
            conn.commit()
            self.numero = cursor.lastrowid
            print(f"Asiento guardado con número: {self.numero}") # mensaje de depuracion
            
    def reservar(self, numeroReserva):
        if(self.numeroReserva==None):
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE asiento SET numeroReserva = ? WHERE numero = ?",(numeroReserva,self.numero))
                conn.commit()
                self.numeroReserva=numeroReserva
        else:
            return {"Exito":False, "Mensaje": f"El asiento numero: {self.numero} tiene una reserva activa"}