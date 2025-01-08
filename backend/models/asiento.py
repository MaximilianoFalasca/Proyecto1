import sqlite3

class Asiento:
    db_path = "C:/Users/maxi/Desktop/python/Proyecto1/backend/database/aerolineasArgentinas.db"
    
    @classmethod
    def inicializar_db(cls):
        with sqlite3.connect(cls.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS asiento(
                    numero INTEGER AUTOINCREMENT,
                    matricula TEXT NOT NULL UNIQUE,
                    precio REAL NOT NULL,
                    PRIMARY KEY (numero, matricula),
                    FOREIGN KEY (matricula) REFERENCES avion(matricula)
                )               
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ocupa(
                    numeroAsiento INTEGER,
                    matricula TEXT,
                    numeroReserva INTEGER,
                    PRIMARY KEY (matricula, numeroAsiento),
                    FOREIGN KEY (matricula) REFERENCES asiento(matricula),
                    FOREIGN KEY (numeroAsiento) REFERENCES asiento(numero),
                    FOREIGN KEY (numeroReserva) REFERENCES reserva(numero),
                )               
            """)
            conn.commit()
        
    # hago esto para poder consultarlo desde reserva y mandar desde ahi los asientos reservados 
    @classmethod
    def asientos_ocupados_por(cls, numeroReserva):
        with sqlite3.connect(cls.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT a.numero, a.matricula
                FROM ocupa o
                    INNER JOIN asiento a ON (a.numero=o.numeroAsiento)
                WHERE numeroReserva = (?)
            """, (numeroReserva,))
            asientos_ocupados = cursor.fetchall()
            return asientos_ocupados
    
    def __init__(self, matricula, precio):
        self.matricula = matricula
        self.precio = precio
    
    def guardar(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO asiento (matricula, precio) VALUES (?,?,?)",(self.matricula,self.precio))
            conn.commit()
            self.numero = cursor.lastrowid
            
    def estaRelacionadoCon(self,numeroReserva):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 1  
                FROM ocupa o
                WHERE (o.numeroAsiento = ? AND o.matricula = ? AND o.numeroReserva = ?)
            """, (self.numero, self.matricula, numeroReserva))
            respuesta = cursor.fetchone()
            return respuesta
            
    def estaOcupado(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 1  
                FROM ocupa o
                    INNER JOIN esta e ON (e.numeroReserva = o.numeroReserva)
                WHERE (o.numeroAsiento = ? AND o.matricula = ? AND e.fechaFin IS NULL AND e.nombreEstado = 'Paid')
            """, (self.numero, self.matricula))
            respuesta = cursor.fetchone()
            return respuesta
            
    def relacionarConReserva(self, numeroReserva):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            respuesta = self.estaOcupado()
            
            if(respuesta):
                raise ValueError("El asiento ya esta reservado")
            
            cursor.execute("INSERT INTO ocupa (numeroAsiento, matricula, numeroReserva) VALUES (?,?,?)",(self.numero, self.matricula, numeroReserva))
            conn.commit()
            self.numeroReserva=numeroReserva
    
    def cancelarRelacionConReserva(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM ocupa WHERE numeroAsiento = (?) and matricula = (?)",(self.numero, self.matricula))
            conn.commit()