import sqlite3

class Persona:
    db_path = "C:/Users/maxi/Desktop/python/Proyecto1/backend/database/aerolineasArgentinas.db"
    
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
    
    #esto hay que cambiarlo y que admita tener el dni como primary key tambien, aca que me mande el dni.
    #fijarse en el actualizar de pasajero
    @classmethod
    def actualizarPersona(cls, cuil, **datos):
        datos_actualizables = ["nombre","apellido"]
        
        mensaje="UPDATE persona SET "
        for key, value in datos:
            if key in datos_actualizables:
                mensaje+=f"{key} = {value}, "
            else:
                raise ValueError(f"El parametro {key} no es un campo actualizable")
        mensaje=mensaje[:-2]
        
        with sqlite3.connect(cls.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(mensaje)
            conn.commit()
    
    def __init__(self, cuil, nombre, apellido):
        self.cuil=cuil
        self.nombre=nombre
        self.apellido=apellido
        
    def guardar(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT nombre, apellido FROM persona WHERE cuil = ?",(self.cuil,))
            resultado = cursor.fetchall()
            if (len(resultado)>0):
                if((resultado[0]!=self.nombre) or (resultado[1]!=self.apellido)):
                    raise ValueError("Cuil registrado con otros datos")
            cursor.execute("INSERT INTO persona (cuil, nombre, apellido) VALUES (?,?,?)",(self.cuil,self.nombre,self.apellido))
            conn.commit()
            
    