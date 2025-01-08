import sqlite3

class Avion:
    db_path = "C:/Users/maxi/Desktop/python/Proyecto1/backend/database/aerolineasArgentinas.db"
    
    @classmethod
    def inicializar_db(cls):
        with sqlite3.connect(cls.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS avion(
                    matricula TEXT NOT NULL PRIMARY KEY,
                    fechaFabricacion DATE NOT NULL,
                    capacidad INTEGER NOT NULL,
                    nombreModelo TEXT NOT NULL,
                    nombreMarca TEXT NOT NULL
                )               
            """)
            conn.commit()
    
    def __init__(self, matricula, fechaFabricacion, capacidad, nombreModelo, nombreMarca):
        self.matricula = matricula
        self.nombreModelo = nombreModelo
        self.fechaFabricacion = fechaFabricacion
        self.capacidad = capacidad
        self.nombreMarca = nombreMarca
    
    def guardar(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO avion (matricula, capacidad, nombreModelo, fechaFabricacion, nombreMarca) VALUES (?,?,?,?,?)",(self.matricula, self.capacidad,  self.nombreModelo, self.fechaFabricacion, self.nombreMarca))
            conn.commit()