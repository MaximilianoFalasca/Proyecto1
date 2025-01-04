import sqlite3

class Persona:
    db_path = "backend/database/aerolineasArgentinas.py"
    
    @classmethod
    def inicializar_db(cls):
        with sqlite3.connect(cls.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS persona(
                    cuil INTEGER PRIMARY KEY UNIQUE,
                    nombre TEXT NOT NULL,
                    apellido TEXT NOT NULL
                )               
            """)
            conn.commit()
    
    def __init__(self, cuil, nombre, apellido):
        self.cuil=cuil
        self.nombre=nombre
        self.apellido=apellido
        
    def guardar(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM persona WHERE cuil = ?",(self.cuil,))
            if (cursor.fetchone()[0]>0):
                return {"exito":False, "mensaje":f"El cuil {self.cuil} ya esta registrado"}
            cursor.execute("INSERT INTO persona (cuil, nombre, apellido) VALUES (?,?,?)",(self.cuil,self.nombre,self.apellido))
            conn.commit()
            return {"exito":True, "mensaje":"Persona registrada correctamente"}
            
    