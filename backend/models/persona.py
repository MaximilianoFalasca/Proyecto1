import sqlite3
from . import Asiento, Vuelo

class Persona:
    db_path = "C:/Users/maxi/Desktop/python/Proyecto1/backend/database/aerolineasArgentinas.db"
    
    @classmethod
    def inicializar_db(cls):
        with sqlite3.connect(cls.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS persona(
                    dni INTEGER PRIMARY KEY,
                    cuil INTEGER UNIQUE,
                    nombre TEXT NOT NULL,
                    apellido TEXT NOT NULL
                )               
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS asociado(
                    dni INTEGER NOT NULL PRIMARY KEY,
                    numeroTarjeta INTEGER NOT NULL,
                    FOREIGN KEY (dni) REFERENCES persona(dni),
                    FOREIGN KEY (numeroTarjeta) REFERENCES beneficio(nroTarjeta)
                )               
            """)
            conn.commit()
    
    @classmethod
    def obtenerPersona(cls, dni):
        with sqlite3.connect(cls.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                        SELECT p.dni, p.cuil, p.nombre, p.apellido, a.numeroTarjeta 
                        FROM persona p
                            LEFT JOIN asociado a ON (a.dni = p.dni)
                        WHERE p.dni = ?
                    """,(dni,)
                )
            respuesta = cursor.fetchone()
            
            if not respuesta:
                raise ValueError(f"No existe una persona registrada con el dni {dni}")

            return cls(
                dni = respuesta[0],
                cuil = respuesta[1],
                nombre = respuesta[2],
                apellido = respuesta[3],
                numeroTarjeta = respuesta[4]
            )
    
    #esto hay que cambiarlo y que admita tener el dni como primary key tambien, aca que me mande el dni.
    #fijarse en el actualizar de pasajero
    @classmethod
    def actualizarPersona(cls, dni, datos:dict):
        datos_actualizables = ["nombre","apellido"]
        
        mensaje="UPDATE persona SET "
        for key, value in datos.items():
            if key in datos_actualizables:
                mensaje+=f"{key} = '{value}', "
            else:
                raise ValueError(f"El parametro {key} no es un campo actualizable")
        
        mensaje=mensaje[:-2]
        mensaje += f" WHERE dni = '{dni}'"
        
        with sqlite3.connect(cls.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(mensaje)
            conn.commit()
    
    def __init__(self, dni, cuil, nombre, apellido, numeroTarjeta=None):
        self.dni=dni
        self.cuil=cuil
        self.nombre=nombre
        self.apellido=apellido
        self.numeroTarjeta=numeroTarjeta 
        
    def guardar(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT nombre, apellido FROM persona WHERE dni = ?",(self.dni,))

            resultado = cursor.fetchone()  # Cambiar a fetchone para obtener una sola fila
        
            if resultado:  
                nombre, apellido = resultado  # Desempaqueta los valores de la fila
                if nombre != self.nombre or apellido != self.apellido:
                    raise ValueError("Dni registrado con otros datos")
            else:

                cursor.execute("INSERT INTO persona (dni, cuil, nombre, apellido) VALUES (?,?,?,?)",(self.dni, self.cuil,self.nombre,self.apellido))
                
                if(self.numeroTarjeta!=None):
                    cursor.execute(f"INSERT INTO asociado (dni, numeroTarjeta) VALUES (?,?)", (self.dni, self.numeroTarjeta))
                
                conn.commit()
            
    def agregarTarjeta(self, numeroTarjeta):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT 1 FROM beneficio WHERE nroTarjeta = '?'",(numeroTarjeta,))
            resultado = cursor.fetchone()
            
            if resultado:
                raise ValueError("No existe una tarjeta con ese nombre")
            
            if(self.numeroTarjeta==None):
                cursor.execute("INSERT INTO asociado (dni, numeroTarjeta) VALUES (?,?)", (self.dni, numeroTarjeta))
            else:
                cursor.execute(f"UPDATE asociado SET numeroTarjeta = {numeroTarjeta} WHERE dni = {self.dni}")
            conn.commit()
            self.numeroTarjeta=numeroTarjeta
        
    # tenes que consultar los asientos del avion del vuelo que no esten ocupados y compararlos con los que te mandaron, si no estan ocupados
    # creas una reserva con estos asientos y al precio de la reserva a la hora de cambiar el estado a paid tenes que fijarte si la persona tiene
    # tarjeta de descuento y hacerle dicho descuento
    # tenes que verificar que los asientos sean de un solo vuelo tambien, sino se tendrian que sacar varias reservas
    # si se cancelan varias veces los vuelos descontas de los puntos y despues de determinadas veces betas a esa persona y que no pueda viajar mas o algo asi
    def sacarReserva(self, vuelo: Vuelo, asientos: list[Asiento]):
        from . import Pasajero, Reserva, Vuelo
        
        if not all(isinstance(asiento, Asiento) for asiento in asientos):
            return ValueError("Los parametros enviados deben ser instancias de Asiento")
            
        if any(asiento.estaOcupado() for asiento in asientos):
            return ValueError("Los asientos no deben estar ocupados")
        
        if not isinstance(vuelo, Vuelo):
            return ValueError("El vuelo debe ser una instancia de Vuelo")
            
        pasajero = Pasajero.obtenerPasajero(self.dni)
        
        if not pasajero:    
            pasajero = Pasajero(self.cuil, self.nombre, self.apellido, self.dni).guardar()
        
        if not pasajero.puedeVolar(vuelo.fechaYHoraSalida, vuelo.fechaYHoraLlegada):
            raise ValueError("No se puede sacar la reserva en esas fechas")
        
        reserva = Reserva(self.dni, vuelo.nro, vuelo.fechaYHoraSalida, asientos)
        
        reserva.guardar()
        
        return reserva