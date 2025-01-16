import sqlite3
from datetime import datetime

class Vuelo:
    db_path = "C:/Users/maxi/Desktop/python/Proyecto1/backend/database/aerolineasArgentinas.db"
    
    @classmethod
    def inicializar_db(cls):
        with sqlite3.connect(cls.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS vuelo(
                    nro INTEGER NOT NULL,
                    fechaYHoraSalida DATE NOT NULL,
                    fechaYHoraLlegada DATE NOT NULL,
                    matricula INTEGER NOT NULL,
                    codigoAeropuertoSalida INTEGER NOT NULL,
                    codigoAeropuertoLlegada INTEGER NOT NULL,
                    PRIMARY KEY (nro, fechaYHoraSalida),
                    FOREIGN KEY (matricula) REFERENCES avion(matricula),
                    FOREIGN KEY (codigoAeropuertoSalida) REFERENCES aeropuerto(codigoAeropuertoSalida),
                    FOREIGN KEY (codigoAeropuertoLlegada) REFERENCES aeropuerto(codigoAeropuertoLlegada)
                )               
            """)
            conn.commit()
            
    @classmethod
    def obtenerVuelo(cls, nro, fechaYHoraSalida):
        with sqlite3.connect(cls.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM vuelo WHERE nro = (?) and fechaYHoraSalida = (?)",(nro,fechaYHoraSalida))
            respuesta = cursor.fetchone()
            
            if not (respuesta):
                raise ValueError("No se encontro un vuelo con ese nro y/o fecha de salida")
            
            avion = cls( 
                nro = nro,
                fechaYHoraSalida = fechaYHoraSalida,
                fechaYHoraLlegada= respuesta[2],
                matricula = respuesta[3],
                codigoAeropuertoSalida = respuesta[4],
                codigoAeropuertoLlegada = respuesta[5],
            )
            
            return avion
    
    @classmethod
    def obtenerTodos(cls):
        with sqlite3.connect(cls.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM vuelo")
            vuelos = cursor.fetchall()
            vuelosP = []
            
            for vuelo in vuelos:
                v = cls( 
                    nro = vuelo[0],
                    fechaYHoraSalida = vuelo[1],
                    fechaYHoraLlegada = vuelo[2],
                    matricula = vuelo[3],
                    codigoAeropuertoSalida = vuelo[4],
                    codigoAeropuertoLlegada = vuelo[5],
                )
                vuelosP.append(v)
            
            return  vuelosP
            
    @classmethod
    def eliminarVuelo(cls, nro, fechaYHoraSalida):
        with sqlite3.connect(cls.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM vuelo WHERE nro = (?) and fechaYHoraSalida = (?)",(nro, fechaYHoraSalida))
            conn.commit()
    
    def __init__(self, nro, fechaYHoraSalida, fechaYHoraLlegada, matricula, codigoAeropuertoSalida, codigoAeropuertoLlegada):
        self.nro = nro
        self.fechaYHoraSalida = fechaYHoraSalida
        self.fechaYHoraLlegada = fechaYHoraLlegada
        self.matricula = matricula
        self.codigoAeropuertoSalida = codigoAeropuertoSalida
        self.codigoAeropuertoLlegada = codigoAeropuertoLlegada
    
    def guardar(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO vuelo (nro, fechaYHoraSalida, fechaYHoraLlegada, matricula, codigoAeropuertoSalida, codigoAeropuertoLlegada) VALUES (?,?,?,?,?,?)",(self.nro, self.fechaYHoraSalida, self.fechaYHoraLlegada, self.matricula, self.codigoAeropuertoSalida, self.codigoAeropuertoLlegada))
            conn.commit()
            
    def toString(self):
        print(f"self.nro : {self.nro}, self.fechaYHoraSalida : {self.fechaYHoraSalida}, self.fechaYHoraLlegada : {self.fechaYHoraLlegada}, self.matricula : {self.matricula}, self.codigoAeropuertoSalida : {self.codigoAeropuertoSalida}, self.codigoAeropuertoLlegada : {self.codigoAeropuertoLlegada}")