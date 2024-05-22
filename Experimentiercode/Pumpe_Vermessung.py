from MOSFET_Classdefinition import MOSFET_Steuerung
import time

pump = MOSFET_Steuerung(pin=17, tastgrad=39)

start_time = time.time() # Startzeit speichern

try:
    while True:
        pump.start()

except KeyboardInterrupt:
    pump.stop()
    end_time = time.time() # Endzeit speichern
    elapsed_time = end_time - start_time # Pumpzeit berechnen
    print(f"Laufzeit: {elapsed_time:.2f} Sekunden")


