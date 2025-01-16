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
                    legajo INTEGER PRIMARY KEY AUTOINCREMENT,
                    dni INTEGER UNIQUE NOT NULL,
                    rol TEXT NOT NULL,
                    horasAcumuladas REAL NOT NULL,
                    nroVuelo INTEGER NOT NULL,
                    fechaYHoraSalida DATE NOT NULL,
                    FOREIGN KEY (nroVuelo, fechaYHoraSalida) REFERENCES vuelo(nro, fechaYHoraSalida)
                )               
            """)
            conn.commit()
            
    @classmethod
    def eliminarTripulacion(cls, legajo):
        with sqlite3.connect(cls.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tripulacion WHERE legajo = (?)",(legajo,))
            conn.commit()
            
    @classmethod
    def obtenerTripulacion(cls, legajo):
        with sqlite3.connect(cls.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tripulacion t INNER JOIN persona p ON (p.dni = t.dni) WHERE t.legajo = (?)",(legajo,))
            respuesta = cursor.fetchone()
            
            if not (respuesta):
                raise ValueError(f"No existe el miembro de la tripulacion con legajo {legajo}")
            
            tripulacion = cls(
                dni=respuesta[1], 
                nombre=respuesta[6], 
                apellido=respuesta[7],
                nroVuelo=respuesta[4],
                fechaYHoraSalida=respuesta[5],
                rol=respuesta[2], 
                numeroTarjeta=respuesta[8] if len(respuesta)>8 else None,
                horasAcumuladas = respuesta[3],
            )
            tripulacion.legajo = respuesta[0]
            return tripulacion
            
    @classmethod
    def obtenerTodos(cls):
        with sqlite3.connect(cls.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * 
                FROM tripulacion t
                    INNER JOIN persona p ON (p.dni=t.dni)           
            """)
            filas = cursor.fetchall()
            tripulacion = []
            
            for f in filas:
                t = cls(
                    dni=f[1], 
                    nombre=f[6], 
                    apellido=f[7],
                    nroVuelo=f[4],
                    fechaYHoraSalida=f[5],
                    rol=f[2], 
                    numeroTarjeta=f[8] if len(f)>8 else None,
                    horasAcumuladas = f[3],
                )
                t.legajo = f[0]
                
                tripulacion.append(t)
            
            return tripulacion
    
    # al finalizar un vuelo se acumulan las horas y se deja el nroVuelo, fechaYHoraSalida y rol vacios
    # hay que ver eso 
    @classmethod
    def actualizarTripulacion(cls, dni, **datos):
        campos_actualizables=["nroVuelo","fechaYHoraSalida","nombre","apellido","horasAcumuladas","rol"]
        
        mensaje="UPDATE tripulacion SET "
        datos_a_actualizar_padre={}
        
        for campo, valor in datos.items():
            if campo in campos_actualizables:
                mensaje+=f"{campo} = {valor}, "
            else:
                if campo == "nombre" or campo == "apellido":
                    datos_a_actualizar_padre[campo]=valor
                else:
                    raise ValueError(f"El parametro {campo} no es un campo actualizable")

        mensaje = mensaje[:-2]
        mensaje += f" WHERE dni = {dni}"
        
        with sqlite3.connect(cls.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(mensaje)
            conn.commit()
            
        Persona.actualizarPersona(dni,datos_a_actualizar_padre)
            
    def __init__(self, dni, cuil, nombre, apellido, nroVuelo, fechaYHoraSalida, rol, numeroTarjeta=None, horasAcumuladas=None):
        super().__init__(dni, cuil, nombre, apellido, numeroTarjeta)
        super().guardar()
        self.dni = dni
        if (horasAcumuladas != None):
            self.horasAcumuladas = horasAcumuladas
        else:
            self.horasAcumuladas = 0
        self.nroVuelo = nroVuelo
        self.rol = rol
        self.fechaYHoraSalida = fechaYHoraSalida
    
    def guardar(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f"INSERT tripulacion (dni, horasAcumuladas, nroVuelo, fechaYHoraSalida, rol) VALUE (?,?,?,?,?)",(self.dni, self.horasAcumuladas, self.nroVuelo, self.fechaYHoraSalida, self.rol))
            self.legajo=cursor.lastrowid
            conn.commit()