import unittest
from backend import Pasajero
import sqlite3
import tempfile
from datetime import datetime

# Registrar el adaptador para datetime antes de inicializar el test
sqlite3.register_adapter(datetime, lambda d: d.strftime('%Y-%m-%d %H:%M:%S'))

class testPasajero(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Usar 'with' para manejar el archivo temporal para que se cierre automaticamente cuando ya no lo utilizamos
        with tempfile.NamedTemporaryFile(delete=False) as db_file:
            cls.db_file = db_file.name
        Pasajero.db_path = cls.db_file
        Pasajero.inicializar_db()
        cls.pasajero = Pasajero(202020, "maximiliano", "falasca", 20202, 1, datetime(2025,1,20,20,0,0))
        cls.pasajero.guardar()
    
    def setUp(self):
        with sqlite3.connect(Pasajero.db_path) as conn:
            cursor=conn.cursor()
            cursor.execute("DELETE FROM pasajero")
            conn.commit()
            
    def test_agregar_tarjeta(self):
        with sqlite3.connect(Pasajero.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT 1 FROM asociado WHERE dni = {self.pasajero.dni}")
            resultado=cursor.fetchone()
            
            #verificamos que todavia no hay ninguna tarjeta asociada
            self.assertIsNone(resultado)
            
            self.pasajero.agregarTarjeta(1)
            
            cursor.execute(f"SELECT numeroTarjeta FROM asociado WHERE dni = {self.pasajero.dni}")
            resultado=cursor.fetchall()
            
            #verificamos que se haya guardado una sola tarjeta asociada
            self.assertEqual(1,len(resultado))
            
            self.pasajero.agregarTarjeta(2)
            
            cursor.execute(f"SELECT numeroTarjeta FROM asociado WHERE dni = {self.pasajero.dni}")
            resultado2=cursor.fetchall()
            
            #verificamos que hay 1 sola tarjeta asociada y que el numero cambio
            self.assertEqual(1,len(resultado2))
            self.assertNotEqual(resultado, resultado2) 
            
    def test_guardar_pasajero_registrado(self):
        pasajero1 = Pasajero(202020, "aaa", "bb", 20202, 1, datetime(2025,1,20,20,0,0))
        resultado = pasajero1.guardar()
        
        self.assertFalse(resultado["exito"])
            
if __name__ == "__main__":
    unittest.main()