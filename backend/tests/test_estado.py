import unittest
from backend import Estado
import sqlite3
import tempfile

class TestEstado(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Esta función se ejecuta una vez antes de todas las pruebas."""
        cls.db_file = tempfile.NamedTemporaryFile(delete=False)
        Estado.db_path = cls.db_file.name
        Estado.inicializar_db()
        
    def setUp(self):
        """Esta función se ejecuta antes de cada prueba."""
        # Limpiar la base de datos antes de cada prueba
        with sqlite3.connect(Estado.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM estado")
            conn.commit()
            
    def test_crear_estado(self):
        """Prueba que un estado pueda ser creado y almacenado en la base de datos."""
        estado = Estado("Paid")
        estado.guardar()
        
        with sqlite3.connect(Estado.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM estado WHERE nombre = 'Paid'")
            resultado = cursor.fetchone()
            
            self.assertIsNotNone(resultado)
    
if __name__ == "__main__":
    unittest.main()
