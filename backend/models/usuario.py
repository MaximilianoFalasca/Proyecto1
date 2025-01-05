import sqlite3

class Usuario:
    db_path = "C:/Users/maxi/Desktop/python/Proyecto1/backend/database/aerolineasArgentinas.db" 

    @classmethod
    def inicializar_bd(cls):
        with sqlite3.connect(cls.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL
                )
            """)
            conn.commit()

    @classmethod
    def obtener_todos(cls):
        with sqlite3.connect(cls.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, email FROM usuarios")
            filas = cursor.fetchall()
            return [cls(id=fila[0], nombre=fila[1], email=fila[2]) for fila in filas]

    def __init__(self, id=None, nombre=None, email=None):
        self.id = id
        self.nombre = nombre
        self.email = email

    def guardar(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuarios (nombre, email) VALUES (?, ?)", (self.nombre, self.email))
            self.id = cursor.lastrowid
            conn.commit()
