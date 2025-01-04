import sqlite3
from .persona import Persona

class Pasajero(Persona):
    db_path = ""
    
    @classmethod
    def inicializar_db(cls):
        super().inicializar_db(cls.db_path)
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
                    dni INTEGER NOT NULL,
                    numeroTarjeta INTEGER NOT NULL,
                    PRIMARY KEY(dni, numeroTarjeta),
                    FOREIGN KEY (dni) REFERENCES pasajero(dni),
                    FOREIGN KEY (numeroTarjeta) REFERENCES beneficio(nroTarjeta)
                )               
            """)
            conn.commit() 
    
    def __init__(self, cuil, nombre, apellido, dni, numeroVuelo, fechaYHoraSalida, telefono=None, mail=None, numeroTarjeta=None):
        super().__init__(cuil, nombre, apellido)
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
            #validar si el pasajero ya existe en la tabla.
            cursor.execute(f"INSERT INTO pasajero (dni, telefono, mail, cuil, numeroVuelo, fechaYHoraSalida) VALUES (?,?,?,?,?,?)",
                           (self.dni, self.telefono, self.mail, self.cuil, self.numeroVuelo, self.fechaYHoraSalida))
            conn.commit()
            return {"exito": True, "mensaje": "Pasajero registrado correctamente"}
        
    def agregarTarjeta(self, numeroTarjeta):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if(self.numeroTarjeta==None):
                cursor.execute("INSERT INTO asociado (dni, numeroTarjeta) VALUES (?,?)", (self.dni, numeroTarjeta))
            else:
                cursor.execute(f"UPDATE asociado SET numeroTarjeta = {numeroTarjeta} WHERE dni = {self.dni}")
            conn.commit()
            self.numeroTarjeta=numeroTarjeta