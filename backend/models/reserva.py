import sqlite3
from .estados import validarEstado
from .asiento import Asiento
import datetime

# tengo lio con los estados, tengo que revisar bien porque cada dia pensaba dif, hay que documentar sobre como va a funcionar

# el estado pending hace referencia a cuando una transaccion no se cerro, esta modificando datos
# esta el pagada y cancelada.

# tengo un problema y es cuando esta en estado pending y quiero obtener la reserva, los asientos no se reservaron todavia pero se tendria que guardar
# igual en la db los asientos pretendidos a reservar y se lo tendria que retornar

# podemos mirar los asientos ocupados como todos aquellos que tienen una relacion con una reserva y ademas el estado de la misma es paid. Si es pending el asiento tiene una relacion
# con ese asiento pero no esta reservado
class Reserva:
    db_path = "C:/Users/maxi/Desktop/python/Proyecto1/backend/database/aerolineasArgentinas.db"

    @classmethod
    def inicializar_bd(cls):
        with sqlite3.connect(cls.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reserva(
                    numero INTEGER PRIMARY KEY AUTOINCREMENT,
                    numeroVuelo INTEGER NOT NULL,
                    fechaYHoraSalida DATE NOT NULL,
                    fecha DATE NOT NULL,
                    precio REAL NOT NULL,
                    dni INTEGER NOT NULL,
                    FOREIGN KEY (dni) REFERENCES pasajero(dni),
                    FOREIGN KEY (numeroVuelo) REFERENCES vuelo(nro),
                    FOREIGN KEY (fechaYHoraSalida) REFERENCES vuelo(nro)
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
            
    @classmethod
    def obtenerTodos(cls):
        with sqlite3.connect(cls.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                    SELECT r.numero, r.fecha, e.nombreEstado, r.dni, r.numeroVuelo, r.fechaYHoraSalida
                    FROM reserva r
                        INNER JOIN esta e ON (e.numeroReserva = r.numero)
                """)       
            
            reservas = cursor.fetchall()
            reservas_con_asientos = []
            
            for reserva in reservas:
                asientos = Asiento.asientos_ocupados_por(reserva[0])
                reserva_nueva = cls(
                    dni = reserva[3],
                    numeroVuelo = reserva[4],
                    fechaYHoraSalida = reserva[5],
                    asientos = Asiento.asientos_ocupados_por(reserva[0])
                )
                reserva_nueva.fecha = reserva[1]
                reserva_nueva.numero = reserva[0]
                reserva_nueva.estado = reserva[2]
                
                reservas_con_asientos.append(reserva_nueva)
            return reservas_con_asientos
            
            
    #vamos a inicializar una reserva e insertarle los datos que no se haga en el init directamente, se crea una funcion en 
    #asiento para ver los que estan reservados por uno mismo
    
    # la reserva que retorne tiene que tener numero, fecha, precio, estadoActual y asientos
    # puede que esta consulta se haga en pending todavia, no hace falta que se pague, en cuyo caso los asientos no estan reservados pero se retornan igual
    
    # tengo un problema y es cuando esta en estado pending y quiero obtener la reserva, los asientos no se reservaron todavia pero se tendria que guardar
    # igual en la db los asientos pretendidos a reservar y se lo tendria que retornar
    @classmethod
    def obtenerReserva(cls, numero):
        with sqlite3.connect(cls.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                    SELECT r.fecha, e.nombreEstado, r.dni, r.numeroVuelo, r.fechaYHoraSalida
                    FROM reserva r
                        INNER JOIN esta e ON (e.numeroReserva = r.numero)
                    WHERE r.numero = (?)
                """,(numero,)
            )
            respuesta = cursor.fetchone()
            
            if not respuesta:
                raise ValueError(f"No existe una reserva con el numero {numero}")
            
            asientos = Asiento.asientos_ocupados_por(numero)
    
            reserva = cls(
                dni = respuesta[2],
                numeroVuelo= respuesta[3],
                fechaYHoraSalida = respuesta[4],
                asientos = asientos
            )
            
            reserva.fecha = respuesta[0]
            reserva.numero = numero
            reserva.estado = respuesta[1]

            return reserva
        
    @classmethod
    def eliminarReserva(cls,numero):
        with sqlite3.connect(cls.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM reserva WHERE numero = ?",(numero, ))
            cursor.execute("DELETE FROM ocupa WHERE numeroReserva = ?",(numero, ))
            conn.commit()
    
    def _inicializarEstado(self):
        if(self.numero!=None):
            with sqlite3.connect(self.db_path) as conn:
                cursor=conn.cursor()
                cursor.execute("INSERT INTO esta (numeroReserva, nombreEstado, fechaInicio, fechaFin) VALUES (?,?,?,?)",(self.numero, 'Pending', self.fecha, None))
                conn.commit()
                self.estado='Pending'
        else:
            raise ValueError("La reserva tiene que estar inicializada previamente")
                
    # no hacemos directamente el guardar aca para que se pueda provar el objeto sin tener que interactuar con la db
    def __init__(self, dni, numeroVuelo, fechaYHoraSalida, asientos=None):
        self.dni = dni
        self.numeroVuelo = numeroVuelo
        self.fechaYHoraSalida = fechaYHoraSalida
        self.fecha = datetime.datetime.now()
        self.precio = 0
        self._asientos = []
        self.numero = None
        self.agregarAsientos(asientos)

    # tengo que verificar que cuando ya se pago o cuando este cancelado no pueda seguir agregando asientos.
    def agregarAsientos(self, asientos):
        for asiento in asientos: 
            if isinstance(asiento, Asiento) and (asiento not in self._asientos):
                self._asientos.append(asiento)
                self.precio+=asiento.precio
                if self.numero != None and not (asiento.estaRelacionadoCon(self.numero)):
                    asiento.relacionarConReserva(self.numero)
                if(self.numero != None):
                    with sqlite3.connect(self.db_path) as conn:
                        cursor = conn.cursor()
                        cursor.execute("UPDATE reserva SET precio = (?) WHERE numero = (?)",(self.precio, self.numero))
                        conn.commit()
    
    # para cuando una persona este cambiando los datos de la reserva mientras esta en pending
    def cambiarAsientos(self, asientos):
        if(self.estado=='Pending'):
            for asiento in self._asientos:
                if(asiento not in asientos):
                    self._asientos.remove(asiento)
                    
                    if(isinstance(asiento,Asiento)):
                        self.precio-=asiento.precio
                        asiento.cancelarRelacionConReserva(self.numero)
            
            self.agregarAsientos(asientos)
        else:
            raise ValueError(f'Si la reserva esta en {self.estado} no se pueden cambiar los asientos')
        
    @property
    def asientos(self):
        """Getter de asientos: devuelve la lista de asientos"""
        return self._asientos

    # Propiedad para 'asientos' que no permite modificar directamente el atributo
    @asientos.setter
    def asientos(self, value):
        """Setter de asientos: no permite modificar directamente la lista de asientos"""
        raise AttributeError("No se puede modificar directamente la lista de asientos. Usa 'cambiarAsientos o agregarAsientos'.")

    # tengo que verificar que no se haga varias veces
    def guardar(self):
        if(self.numero==None):
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO reserva (dni, fecha, precio, numeroVuelo, fechaYHoraSalida) VALUES (?,?,?,?,?)", (self.dni, self.fecha, self.precio, self.numeroVuelo, self.fechaYHoraSalida))
                self.numero = cursor.lastrowid
                # esto no se hace todavia porque no se confirmo el pago, estamos en pending todavia
                # for asiento in self._asientos:
                #     if isinstance(asiento, Asiento):
                #         asiento.reservar(self.numero)
                
                conn.commit()
            for asiento in self.asientos:
                if not (asiento.estaRelacionadoCon(self.numero)):
                    asiento.relacionarConReserva(self.numero)
            self._inicializarEstado()
            return self       
        else:
            raise ValueError("La reserva ya esta guardada") 

    # tengo que verificar que una reserva cuando pase a cancelled no pueda volver a cambiar de estado
    def cambiarEstado(self, estado):
        from .pasajero import Pasajero
        
        if(not validarEstado(estado)):
            raise ValueError('El estado ingresado no es valido')
        
        if(self.numero==None):
            raise ValueError('La reserva debe estar inicializada previamente')
        
        if(self.estado==estado):
            raise ValueError('El estado ingresado ya se encuentra registrado')
        
        if(self.estado=='Cancelled'):
            raise ValueError("La reserva se encuentra cancelada, no se puede modificar su estado")
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            self.estado = estado
            
            fecha = datetime.datetime.now()
            fecha_sql = f"{fecha.year}-{fecha.month}-{fecha.day}"
            
            cursor.execute(f"UPDATE esta SET fechaFin = ? WHERE numeroReserva = ? and nombreEstado = ?",(fecha_sql, self.numero, self.estado))
            cursor.execute("INSERT INTO esta (numeroReserva, nombreEstado, fechaInicio, fechaFin) VALUES (?,?,?,?)", (self.numero, estado, fecha_sql, None))
            
            conn.commit() 
            