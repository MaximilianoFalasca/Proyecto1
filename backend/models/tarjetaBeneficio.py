import sqlite3

class TarjetaBeneficio:
    db_path = "C:/Users/maxi/Desktop/python/Proyecto1/backend/database/aerolineasArgentinas.db"

    @classmethod
    def inicializar_bd(cls):
        with sqlite3.connect(cls.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS beneficio (
                    nroTarjeta INTEGER PRIMARY KEY NOT NULL,
                    puntos REAL NOT NULL
                )
            """)
            conn.commit()
            
    @classmethod
    def obtenerTodos(cls):
        with sqlite3.connect(cls.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM beneficio")
            filas = cursor.fetchall()
            # devuelvo objetos beneficio (se crean en esta parte: cls(nroTarjeta=fila[0], puntos=fila[1])) por cada una de las tuplas devueltas 
            return [cls(nroTarjeta=fila[0], puntos=fila[1]) for fila in filas]
        
    @classmethod
    def obtener_por_nro_tarjeta(cls, nroTarjeta):
        with sqlite3.connect(cls.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                SELECT *
                FROM beneficio b
                WHERE b.nroTarjeta = '{nroTarjeta}'
            """)
            beneficio = cursor.fetchone()
            return cls(nroTarjeta=beneficio[0], puntos=beneficio[1])
        
    @classmethod
    def actualizarTarjeta(cls, nroTarjeta, puntos):
        with sqlite3.connect(cls.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE beneficio SET puntos = ? WHERE nroTarjeta = ?", (puntos, nroTarjeta))
            conn.commit()

    @classmethod
    def eliminarTarjeta(cls, nroTarjeta):
        with sqlite3.connect(cls.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM beneficio WHERE nroTarjeta = ?", (nroTarjeta,))
            conn.commit()

    def __init__(self, nroTarjeta, puntos=None):
        self.nroTarjeta=nroTarjeta
        if puntos==None:
            self.puntos=0
        else:
            self.puntos=puntos

    def guardar(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO beneficio (nroTarjeta, puntos) VALUES (? ,?)",(self.nroTarjeta,self.puntos))
            conn.commit()
    
    def calcular_descuento(self, monto):
        descuento=0
        if (self.puntos>=10000):
            descuento=monto*0.1
        return descuento