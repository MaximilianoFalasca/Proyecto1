import sqlite3

class Aeropuerto:
    db_path = "C:/Users/maxi/Desktop/python/Proyecto1/backend/database/aerolineasArgentinas.db"
    
    @classmethod
    def inicializar_db(cls):
        with sqlite3.connect(cls.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Aeropuerto(
                    codigo INTEGER AUTOINCREMENT PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    nombreCiudad TEXT NOT NULL,
                    nombrePaiz TEXT NOT NULL
                )               
            """)
            conn.commit()
    
    def __init__(self, codigo, nombre, nombreCiudad, nombrePaiz):
        self.codigo = codigo
        self.nombre = nombre
        self.nombreCiudad = nombreCiudad
        self.capacidnombrePaizad = nombrePaiz
    
    def guardar(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Aeropuerto (codigo, nombre, nombreCiudad, nombrePaiz) VALUES (?,?,?,?)",(self.codigo, self.nombre,  self.nombreCiudad, self.nombrePaiz))
            conn.commit()