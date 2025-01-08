tendria que hacer un archivo que contenga la ubicacion de la db y hacer que github no pueda acceder a ella.
tengo que hacer los routes y los test que me faltan.

para comentar varias lineas a la vez es con ctrl + }

## iniciar entorno virtual

.\venv\Scripts\activate

## desactivar entorno virtual

deactivate

## instalar requerimientos

pip install -r requirements.txt

## iniciar el servidor (desde \backend):

python app.py

## ejecutar los test (desde \Proyecto)

python -m unittest discover backend/tests

o

python -m backend.tests.test_asiento


## consigna

Se desean modelar los datos relacionados con vuelos, pasajeros, tripulación y reservas de Aerolíneas Argentinas. De cada vuelo se conoce número de vuelo (que se repite para diferentes fechas de salida), aeropuerto de origen, aeropuerto de destino, fecha y hora de salida, fecha y hora de llegada (se cargan una vez que arriba), el avión que realizará el vuelo, los miembros de la tripulación asignados y los pasajeros que viajarán. De cada avión se conoce su matrícula (única), su marca (Boeing, Airbus, Embraer, etc), su modelo, su año de fabricación y su capacidad (cantidad de asientos para pasajeros). De cada aeropuerto se conoce un código único (por ejemplo, para el aeropuerto de Bariloche, el código es BRC), el nombre del aeropuerto, la ciudad y el país en el que se encuentra. Tenga en cuenta que un mismo nombre de ciudad se puede repetir para diferentes países.

De los miembros de la tripulación se conoce su nombre, apellido, CUIL, número de legajo (único), horas de vuelo acumuladas y uno o más roles que pueden cumplir. En cambio, de los pasajeros que viajarán se conoce su nombre, apellido, CUIL, DNI, teléfono, email y, en caso de estar asociados al programa de beneficios de la aerolínea, los puntos acumulados hasta el momento y el nivel de la tarjeta de beneficios.

Para viajar en un vuelo, los pasajeros necesitan hacer una reserva. De la reserva se conocen el número único de reserva, fecha de reserva, los asientos asignados a cada pasajero y el estado (pendiente, pagada, cancelada, etc). Además, se requiere llevar un histórico de los cambios de estado de cada reserva, registrando el día en que la reserva permaneció en cada estado. Esto permitirá llevar un seguimiento detallado del ciclo de vida de cada reserva.

---

### **Casos límite a considerar:**
1. **Capacidad de pasajeros:**
   - No puede registrarse más pasajeros que la capacidad del avión.

2. **Histórico de reservas:**
   - Permitir mantener un registro de cambios de estado (por ejemplo, de pendiente a pagada o cancelada).

3. **Puntos de fidelidad:**
   - Los pasajeros acumulan puntos al completar vuelos.
   - al llegar a los 10.000 puntos es el nivel mas alto de fidelidad.
   - al llegar al nivel mas alto de la tarjeta se aplica un 10% de descuento en sus vuelos con gasto superior a 100.000.
   - Si un pasajero cancela su reserva, pierde los puntos acumulados.

4. **Asignación de asientos:**
   - No puede asignarse el mismo asiento a más de un pasajero en el mismo vuelo.

5. **Cambio de estado de vuelos:**
   - Un vuelo solo puede marcarse como "completado" cuando ha llegado a destino.
   - Un vuelo debe cancelarse si no hay reservas confirmadas al menos 24 horas antes de la salida.

---

### **Funciones a implementar:**

#### 1. **Cargar saldo para un pasajero (Programa de beneficios):**
   - Dado un pasajero y un monto, incrementa su saldo de puntos.
   - Regla: Los pasajeros acumulan **1 punto por cada $10 gastados**. Si el pasajero tiene el nivel más alto de la tarjeta, acumula un **10% extra de puntos.**

#### 2. **Dar de alta un vuelo:**
   - Recibe el número de vuelo, origen, destino, avión asignado, fecha y hora de salida/llegada.
   - Valida que:
     - El avión no esté asignado a otro vuelo en la misma fecha.
     - El origen y destino sean diferentes.

#### 3. **Registrar un pasajero para un vuelo:**
   - Recibe un pasajero y un vuelo.
   - Valida que:
     - El pasajero tenga una reserva activa y pagada.
     - Haya asientos disponibles.
     - El pasajero no esté registrado en otro vuelo que despegue o aterrice en horarios que se superpongan con este.

#### 4. **Procesar un vuelo:**
   - Cambia el estado del vuelo a "completado".
   - Asigna puntos de fidelidad a los pasajeros registrados.
   - Incrementa las horas de vuelo acumuladas para los miembros de la tripulación.
   - Si el vuelo se cancela, devuelve los puntos a los pasajeros y los quita del historial del vuelo.

---

### **Ejemplo de reglas específicas:**

#### **Asignación de puntos de fidelidad (caso límite):**
- Si un pasajero tiene reservas en múltiples vuelos, los puntos solo se acumulan al completarse cada vuelo.
- Si un vuelo se cancela, los puntos no se asignan.

#### **Cambio de estado en vuelos:**
- Estado inicial: "Programado".
- Si faltan menos de 24 horas y no hay reservas confirmadas, pasa a "Cancelado".
- Al aterrizar, pasa a "Completado".

---

### **Sugerencias de implementación (con casos límite):**

1. **Validación de la capacidad del avión:**
   - Al registrar pasajeros en un vuelo, verifica que no se exceda la capacidad del avión.
   - Si un pasajero cancela su reserva, libera el asiento correspondiente.

2. **Restricciones en fechas y horarios:**
   - Valida que no se registren vuelos que se superpongan en horarios para el mismo avión.

3. **Programa de beneficios:**
   - Bonificación de puntos extra a pasajeros frecuentes (por ejemplo, más de 10 vuelos al año).

4. **Reservas pendientes:**
   - Al registrar un vuelo, verifica que las reservas estén confirmadas al menos 24 horas antes de la salida para evitar la cancelación.

---

implementar grafo para obtner el camino con menor costo (puede ser plata o tiempo) hasta llegar a un destino desde un origen.