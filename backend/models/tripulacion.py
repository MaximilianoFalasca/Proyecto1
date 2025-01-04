import sqlite3

class Tripulacion:
    db_path=''
    
    @classmethod
    def inicializar_db(cls):
        with sqlite3.connect(cls.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tripulacion(
                    legajo INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                    horasAcumuladas REAL NOT NULL,
                    cuil INTEGER NOT NULL UNIQUE,
                    nroVuelo INTEGER NOT NULL,
                    fechaYHoraSalida DATE NOT NULL,
                    FOREIGN KEY (nroVuelo, fechaYHoraSalida) REFERENCES vuelo(nro, fechaYHoraSalida)
                )               
            """)
            conn.commit()
            
    def __init__(self, horasAcumuladas, cuil, nroVuelo, fechaYHoraSalida):
        self.horasAcumuladas = horasAcumuladas
        self.cuil = cuil
        self.nroVuelo = nroVuelo
        self.fechaYHoraSalida = fechaYHoraSalida
    
    def guardar(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f"INSERT tripulacion (horasAcumuladas, cuil, nroVuelo, fechaYHoraSalida) VALUE (?,?,?,?)",(self.horasAcumuladas,self.cuil,self.nroVuelo,self.fechaYHoraSalida))
            self.legajo=cursor.lastrowid
            conn.commit()