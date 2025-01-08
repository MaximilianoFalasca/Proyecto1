import unittest
from backend import Asiento
import sqlite3
import tempfile

class TestAsiento(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Esta función se ejecuta una vez antes de todas las pruebas."""
        # Inicializamos la base de datos, creando las tablas necesarias
        cls.db_file = tempfile.NamedTemporaryFile(delete=False)
        Asiento.db_path = cls.db_file.name
        Asiento.inicializar_db()
    
    def setUp(self):
        """Esta función se ejecuta antes de cada prueba."""
        # Limpiar la base de datos antes de cada prueba
        with sqlite3.connect(Asiento.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM asiento")
            conn.commit()

    def test_crear_asiento(self):
        """Prueba que un asiento pueda ser creado y almacenado en la base de datos."""
        asiento = Asiento(matricula="ABC123", precio=100)
        asiento.guardar()
        
        # Verificamos si el asiento fue correctamente guardado en la base de datos
        with sqlite3.connect(Asiento.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM asiento WHERE numero = ?", (asiento.numero,))
            resultado = cursor.fetchone()
            
            self.assertIsNotNone(resultado) 
            self.assertEqual(resultado[2], "ABC123")  
            self.assertEqual(resultado[3], 100)  

    
    # def test_reservar_asiento(self):
    #     """Prueba que un asiento pueda ser reservado correctamente."""
    #     asiento = Asiento(matricula="DEF456", precio=150)
    #     asiento.guardar()
        
    #     # Reservamos el asiento
    #     reserva_id = 1  # Id de reserva ficticio
    #     resultado_reserva = asiento.reservar(reserva_id)
        
    #     # Verificamos si la reserva fue exitosa
    #     self.assertTrue(resultado_reserva["Exito"]) 
    #     self.assertEqual(asiento.numeroReserva, reserva_id) 

    #     # Verificamos en la base de datos si el asiento está reservado
    #     with sqlite3.connect(Asiento.db_path) as conn:
    #         cursor = conn.cursor()
    #         cursor.execute("SELECT numeroReserva FROM asiento WHERE numero = ?", (asiento.numero,))
    #         resultado = cursor.fetchone()
    #         self.assertEqual(resultado[0], reserva_id) 

    def test_reservar_asiento_ya_reservado(self):
        """Prueba que no se pueda reservar un asiento que ya está reservado."""
        asiento = Asiento(matricula="GHI789", precio=200)
        asiento.guardar()
        
        # Reservamos el asiento con un id de reserva
        resultado_reserva1 = asiento.reservar(1)
        
        # Intentamos reservar nuevamente el mismo asiento
        resultado_reserva2 = asiento.reservar(2)
    
        # Verificamos que la reserva no haya sido exitosa
        self.assertTrue(resultado_reserva1["Exito"])
        self.assertEqual(resultado_reserva2["Mensaje"], f" Se reservo el asiento numero: {asiento.numero} exitosamente")
        self.assertFalse(resultado_reserva2["Exito"])  # El asiento ya está reservado
        self.assertEqual(resultado_reserva2["Mensaje"], f"El asiento numero: {asiento.numero} tiene una reserva activa")

    @classmethod
    def tearDownClass(cls):
        """Esta función se ejecuta una vez después de todas las pruebas."""
        with sqlite3.connect(Asiento.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS asiento") 
            conn.commit()

if __name__ == "__main__":
    unittest.main()
