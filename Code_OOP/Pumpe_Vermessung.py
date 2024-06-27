from MOSFET_Classdefinition import MOSFET_control
import time
from PARAMETERS_Definition import parameters

pump = MOSFET_control(pin=parameters.fertilizerpump_pin, dutycycle=parameters.fertilizerpump_dutycycle, startuptime=parameters.fertilizerpump_startuptime, actiontime=parameters.fertilizerpump_actiontime)

start_time = time.time() # Startzeit speichern

try:
    while True:
        pump.start()

except KeyboardInterrupt:
    pump.stop()
    end_time = time.time() # Endzeit speichern
    elapsed_time = end_time - start_time # Pumpzeit berechnen
    print(f"Laufzeit: {elapsed_time:.2f} Sekunden")

    # Pumpzeit in Datei abspeichern
    with open("laufzeit_fluten.txt", "a") as file:  # Datei im Append-Modus öffnen
        file.write(f"Laufzeit: {elapsed_time:.2f} Sekunden\n")


