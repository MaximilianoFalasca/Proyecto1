import sqlite3
from .persona import Persona

class Tripulacion(Persona):
    db_path='C:/Users/maxi/Desktop/python/Proyecto1/backend/database/aerolineasArgentinas.db'
    
    @classmethod
    def inicializar_db(cls):
        with sqlite3.connect(cls.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tripulacion(
                    legajo INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                    rol TEXT,
                    horasAcumuladas REAL NOT NULL,
                    nroVuelo INTEGER NOT NULL,
                    fechaYHoraSalida DATE NOT NULL,
                    FOREIGN KEY (nroVuelo, fechaYHoraSalida) REFERENCES vuelo(nro, fechaYHoraSalida)
                )               
            """)
            conn.commit()
            
    def __init__(self, cuil, nombre, apellido , horasAcumuladas, nroVuelo, fechaYHoraSalida):
        super().__init__(cuil, nombre, apellido)
        super().guardar()
        self.horasAcumuladas = horasAcumuladas
        self.nroVuelo = nroVuelo
        self.fechaYHoraSalida = fechaYHoraSalida
    
    def guardar(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f"INSERT tripulacion (horasAcumuladas, cuil, nroVuelo, fechaYHoraSalida) VALUE (?,?,?,?)",(self.horasAcumuladas,self.cuil,self.nroVuelo,self.fechaYHoraSalida))
            self.legajo=cursor.lastrowid
            conn.commit()