import sqlite3
from .persona import Persona
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
                    dni INTEGER NOT NULL UNIQUE PRIMARY KEY,
                    telefono INTEGER,
                    mail TEXT,
                    cuil INTEGER NOT NULL UNIQUE,
                    numeroVuelo INTEGER NOT NULL,
                    fechaYHoraSalida DATE NOT NULL,
                    FOREIGN KEY (cuil) REFERENCES persona(cuil),
                    FOREIGN KEY (numeroVuelo) REFERENCES vuelo(numero),
                    FOREIGN KEY (fechaYHoraSalida) REFERENCES vuelo(fechaYHoraSalida)
                )               
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS asociado(
                    dni INTEGER NOT NULL PRIMARY KEY,
                    numeroTarjeta INTEGER NOT NULL,
                    FOREIGN KEY (dni) REFERENCES pasajero(dni),
                    FOREIGN KEY (numeroTarjeta) REFERENCES beneficio(nroTarjeta)
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
                SELECT * 
                FROM pasajero p
                    INNER JOIN persona pe ON (pe.dni=p.dni)
                    LEFT JOIN asociado a ON (a.dni=p.dni)
                WHERE p.dni = (?)
            """,(dni,))
            respuesta = cursor.fetchone()
            if not (respuesta):
                raise ValueError(f"No existe el pasajero con dni {dni}")
            
            return cls(
                dni=respuesta[0],
                telefono=respuesta[1], 
                mail=respuesta[2], 
                cuil=respuesta[3], 
                numeroVuelo=respuesta[4], 
                fechaYHoraSalida=respuesta[5], 
                nombre=respuesta[6], 
                apellido=respuesta[7], 
                numeroTarjeta=respuesta[8] if len(respuesta)>8 else None
            )
            
    @classmethod
    def obtenerTodos(cls):
        with sqlite3.connect(cls.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * 
                FROM pasajero p
                    LEFT JOIN asociado a ON (a.dni=p.dni)           
            """)
            filas = cursor.fetchall()
            # por cada elemento en filas se intancia un pasajero con los parametros mandados.
            return [
                cls(
                    cuil=fila[0], 
                    nombre=fila[1], 
                    apellido=fila[2], 
                    dni=fila[3], 
                    numeroVuelo=fila[4], 
                    fechaYHoraSalida=fila[5], 
                    telefono=fila[6], 
                    mail=fila[7], 
                    numeroTarjeta=fila[8] if len(fila)>8 else None
                ) for fila in filas
            ]
    
    @classmethod
    def actualizarPasajero(cls, dni, **datos):
        campos_actualizables=["telefono","mail","nombre","apellido"]
        
        # creamos el mensaje para despues ejecutarlo con los parametros enviados, tanto para pasajeros como para persona.
        # verificando que no haya ningun parametro fuera de los campos que se pueden actualizar
        mensaje="UPDATE pasajero SET "
        datos_a_actualizar_padre={}
        
        for campo, valor in datos.items():
            if campo in campos_actualizables:
                mensaje+=f"{campo} = {valor}, "
            else:
                if campo == "nombre" or campo == "apellido":
                    datos_a_actualizar_padre[campo]=valor
                else:
                    raise ValueError(f"El parametro {campo} no es un campo actualizable")

        # cortamos los dos ultimos caracteres (quedaria un ", " de mas) y terminamos la consulta
        mensaje = mensaje[:-2]
        mensaje += f" WHERE dni = {dni}"
        
        with sqlite3.connect(cls.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(mensaje)
            conn.commit()
            
        Persona.actualizarPersona(dni,datos_a_actualizar_padre)
    
    def __init__(self, cuil, nombre, apellido, dni, numeroVuelo, fechaYHoraSalida, telefono=None, mail=None, numeroTarjeta=None):
        if not isinstance(fechaYHoraSalida, datetime):
            raise ValueError("La fecha y hora de salida no tiene un formato valido.")
        if (fechaYHoraSalida.date() <= datetime.now().date()):
            raise ValueError("La fecha y hora de salida es invalida.")
        
        super().__init__(cuil, nombre, apellido)
        try:
            super().guardar()
        except ValueError as e:
            raise ValueError(e.args)
        
        self.dni=dni
        self.numeroVuelo=numeroVuelo
        self.fechaYHoraSalida=fechaYHoraSalida
        self.telefono=telefono
        self.mail=mail
        self.numeroTarjeta=numeroTarjeta    
        
    def guardar(self):
        super().guardar()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute(f"INSERT INTO pasajero (dni, telefono, mail, cuil, numeroVuelo, fechaYHoraSalida) VALUES (?,?,?,?,?,?)",
                           (self.dni, self.telefono, self.mail, self.cuil, self.numeroVuelo, self.fechaYHoraSalida))

            if(self.numeroTarjeta!=None):
                cursor.execute(f"INSERT INTO asociado (dni, numeroTarjeta) VALUES (?,?)", (self.dni, self.numeroTarjeta))
            
            conn.commit()
        
    def agregarTarjeta(self, numeroTarjeta):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if(self.numeroTarjeta==None):
                cursor.execute("INSERT INTO asociado (dni, numeroTarjeta) VALUES (?,?)", (self.dni, numeroTarjeta))
            else:
                cursor.execute(f"UPDATE asociado SET numeroTarjeta = {numeroTarjeta} WHERE dni = {self.dni}")
            conn.commit()
            self.numeroTarjeta=numeroTarjeta