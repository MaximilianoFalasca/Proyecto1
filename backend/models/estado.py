import sqlite3

class Estado:
    db_path=''
    
    @classmethod
    def inicializar_db(cls):
        with sqlite3.connect(cls.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS estado(
                    nombre TEXT NOT NULL PRIMARY KEY
                )               
            """)
            conn.commit()
            
    def __init__(self, nombre):
        self.nombre= nombre
    
    def guardar(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT estado (nombre) VALUE (?)",(self.nombre,))
            conn.commit()