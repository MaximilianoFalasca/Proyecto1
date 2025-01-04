import sqlite3
from .estados import validarEstado
from .asiento import Asiento  # Importamos la clase Asiento
import datetime


class Reserva:
    db_path = "app/database/usuarios.db"

    @classmethod
    def inicializar_bd(cls):
        with sqlite3.connect(cls.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reserva(
                    numero INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha DATE NOT NULL,
                    precio REAL NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ocupa(
                    numeroReserva INTEGER NOT NULL,
                    numeroAsiento INTEGER NOT NULL,
                    PRIMARY KEY (numeroReserva, numeroAsiento),
                    FOREIGN KEY (numeroReserva) REFERENCES reserva(numero),
                    FOREIGN KEY (numeroAsiento) REFERENCES asiento(numero)
                )   
            """)
            #estado seria pendiente de pago, pagada, cancelada, etc.
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS esta(
                    numeroReserva INTEGER NOT NULL,
                    nombreEstado INTEGER NOT NULL,
                    fechaInicio Date NOT NULL,
                    fechaFin DATE,
                    PRIMARY KEY (numeroReserva, nombreEstado),
                    FOREIGN KEY (numeroReserva) REFERENCES reserva(numero),
                    FOREIGN KEY (nombreEstado) REFERENCES estado(nombre)
                )   
            """)
            conn.commit()

    def _inicializarEstado(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor=conn.cursor()
            cursor.execute("INSERT INTO esta (numeroReserva, nombreEstado, fechaInicio, fechaFin) VALUE (?,?,?,?)",(self.numero, 'Pending', self.fecha, None))
            conn.commit()
            self.estado='Pending'
                
    # no hacemos directamente el guardar aca para que se pueda provar el objeto sin tener que interactuar con la db
    def __init__(self, fecha, asientos):
        self.fecha = fecha
        self.precio = 0
        self._asientos = []
        self.agregarAsientos(asientos)

    # tengo que verificar que cuando ya se pago o cuando este cancelado no pueda seguir agregando asientos.
    def agregarAsientos(self, asientos):
        for asiento in asientos: 
            if isinstance(asiento, Asiento) and (asiento not in self._asientos):
                self._asientos.append(asiento)
                self.precio+=asiento.precio
        
    @property
    def asientos(self):
        """Getter de asientos: devuelve la lista de asientos"""
        return self._asientos

    # Propiedad para 'asientos' que no permite modificar directamente el atributo
    @asientos.setter
    def asientos(self, value):
        """Setter de asientos: no permite modificar directamente la lista de asientos"""
        raise AttributeError("No se puede modificar directamente la lista de asientos. Usa 'cambiarAsientos o agregarAsientos'.")
    
    # para cuando una persona este cambiando los datos de la reserva mientras esta en pending
    def cambiarAsientos(self, asientos):
        if(self.estado=='Pending'):
            for asiento in self._asientos:
                if(asiento not in asientos):
                    self._asientos.remove(asiento)
            self.agregarAsientos(asientos)
            return {'Exito':True,'Mensaje':'Cambio de asientos realizado con exito'}
        else:
            return {'Exito':False,'Mensaje':f'Si la reserva esta en {self.estado} no se pueden cambiar los asientos'}

    # tengo que verificar que no se haga varias veces
    def guardar(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO reserva (fecha, precio) VALUES (?, ?)", (self.fecha, self.precio))
            self.numero = cursor.lastrowid
            for asiento in self._asientos:
                if isinstance(asiento, Asiento):
                    asiento.reservar(self.numero)
                cursor.execute("INSERT INTO ocupa (numeroReserva, numeroAsiento) VALUES (?, ?)", (self.numero, asiento.numero))
            conn.commit()
            self._inicializarEstado()
            return self        

    # tengo que verificar que una reserva cuando pase la fecha del vuelo y el estado sea pending se pase a cancelled y que una vez que sea cancelada no pueda volver a hacerse
    def cambiarEstado(self, estado):
        if(not validarEstado(estado)):
            return {'Exito':False,'Mensaje':'El estado ingresado no es valido'}
        
        if(self.numero==None):
            return {'Exito':False,'Mensaje':'La reserva debe estar guardada en la db previamente'}
        
        if(self.estado==estado):
            return {'Exito':False,'Mensaje':'El estado ingresado ya se encuentra registrado'}
            
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            self.estado = estado
            
            fecha = datetime.datetime.now()
            fecha_sql = f"{fecha.year}-{fecha.month}-{fecha.day}"
            
            cursor.execute(f"UPDATE esta SET fechaFin = {fecha_sql} WHERE numeroReserva = {self.numero} and nombreEstado = {self.estado}")
            cursor.execute("INSERT INTO esta (numeroReserva, nombreEstado, fechaInicio, fechaFin) VALUE (?,?,?,?)", (self.numero, estado, fecha_sql, None))
            if(estado=='Paid'):
                mensajes = []
                for asiento in self._asientos:
                    if(isinstance(asiento, Asiento)):
                        mensajes = mensajes.append(asiento.reservar(self.numero))
                    mensajes_negativos = [mensaje for mensaje in mensajes if mensaje["Exito"]==False]
                    
                    # si hay algun asiento que esta ocupado no se registra ninguno de los asientos, retorna el/los mensajes de error
                    if(mensajes_negativos.count()>0):
                        return mensajes_negativos
            # me tengo que fijar si el estado es cancelled tengo que hacer algo.
            conn.commit() 