import sqlite3
from .persona import Persona
from .vuelo import Vuelo
from datetime import datetime

class Pasajero(Persona):
    db_path = "C:/Users/maxi/Desktop/python/Proyecto1/backend/database/aerolineasArgentinas.db"
    
    @classmethod
    def inicializar_db(cls):
        super().inicializar_db()
        with sqlite3.connect(cls.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pasajero(
                    dni INTEGER NOT NULL PRIMARY KEY,
                    telefono INTEGER,
                    mail TEXT,
                    FOREIGN KEY (dni) REFERENCES persona(dni)
                )               
            """)
            conn.commit() 
            
    @classmethod
    def eliminarPasajero(cls, dni):
        with sqlite3.connect(cls.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM pasajero WHERE dni = (?)",(dni,))
            cursor.execute("DELETE FROM asociado WHERE dni = (?)",(dni,))
            conn.commit()
            
    @classmethod
    def obtenerPasajero(cls, dni):
        with sqlite3.connect(cls.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.dni, p.telefono, p.mail, a.numeroTarjeta, pe.cuil, pe.nombre, pe.apellido 
                FROM pasajero p
                    INNER JOIN persona pe ON (pe.dni=p.dni)
                    LEFT JOIN asociado a ON (a.dni=p.dni)
                WHERE p.dni = (?)
            """,(dni,))
            respuesta = cursor.fetchone()
            
            return cls(
                dni=respuesta[0],
                telefono=respuesta[1], 
                mail=respuesta[2], 
                numeroTarjeta=respuesta[3],
                cuil=respuesta[4], 
                nombre=respuesta[5], 
                apellido=respuesta[6]
            )
            
    @classmethod
    def obtenerTodos(cls):
        with sqlite3.connect(cls.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.dni, p.telefono, p.mail, a.numeroTarjeta, pe.cuil, pe.nombre, pe.apellido 
                FROM pasajero p
                    LEFT JOIN asociado a ON (a.dni=p.dni)  
                    INNER JOIN persona pe ON (pe.dni=p.dni)         
            """)
            filas = cursor.fetchall()
            # por cada elemento en filas se intancia un pasajero con los parametros mandados.
            return [
                cls(
                    dni=fila[0],
                    telefono=fila[1], 
                    mail=fila[2], 
                    numeroTarjeta=fila[3],
                    cuil=fila[4], 
                    nombre=fila[5], 
                    apellido=fila[6],
                ) for fila in filas
            ]
    
    @classmethod
    def actualizarPasajero(cls, dni, datos:dict):
        campos_actualizables=["telefono","mail","nombre","apellido"]
        
        # creamos el mensaje para despues ejecutarlo con los parametros enviados, tanto para pasajeros como para persona.
        # verificando que no haya ningun parametro fuera de los campos que se pueden actualizar
        mensaje="UPDATE pasajero SET "
        datos_a_actualizar_padre={}
        
        for campo, valor in datos.items():
            if campo in campos_actualizables:
                if campo == "nombre" or campo == "apellido":
                    datos_a_actualizar_padre[campo]=valor
                else:
                    mensaje+=f"{campo} = '{valor}', "
            else:
                raise ValueError(f"El parametro {campo} no es un campo actualizable")

        # cortamos los dos ultimos caracteres (quedaria un ", " de mas) y terminamos la consulta
        if mensaje != "UPDATE pasajero SET ":
            mensaje = mensaje[:-2]
            mensaje += f" WHERE dni = '{dni}'"
        
            with sqlite3.connect(cls.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(mensaje)
                conn.commit()
        
        if len(datos_a_actualizar_padre) > 0:
            Persona.actualizarPersona(dni,datos_a_actualizar_padre)
    
    def __init__(self, cuil, nombre, apellido, dni, telefono=None, mail=None, numeroTarjeta=None):
        super().__init__(dni, cuil, nombre, apellido, numeroTarjeta)
        try:
            super().guardar()
        except Exception as e:
            raise ValueError(e.args)
        self.telefono=telefono
        self.mail=mail 
        
    def guardar(self):
        super().guardar()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute(f"INSERT INTO pasajero (dni, telefono, mail) VALUES (?,?,?)",
                           (self.dni, self.telefono, self.mail))

            conn.commit()
            
    def puedeVolar(self, fechaSalida, fechaLlegada):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT 1
                FROM reserva r 
                    INNER JOIN vuelo v ON (r.numeroVuelo = v.nro AND r.fechaYHoraSalida = v.fechaYHoraSalida)
                WHERE r.dni = ? AND v.fechaYHoraSalida > DATETIME('now') AND (v.fechaYHoraSalida < ? OR v.fechaYHoraLlegada > ?)
            """,(self.dni, fechaLlegada, fechaSalida))
            respuesta = cursor.fetchone()
            
            return respuesta is None