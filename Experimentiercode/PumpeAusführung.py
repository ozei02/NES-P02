# Erforderliche Bibliotheken importieren
import time
# Importieren der MOSFET_Steuerung Klasse aus MOSFET_Classdefinition um in diesem Skript ein Objekt erstellen zu können
from MOSFET_Classdefinition import MOSFET_Steuerung

# Instanziieren der Düngerpumpe als Objekt der MOSFET Klasse
# Pin je nach Anschluss an den Raspberry anpassen
# Tastgrad je nach Netzteil und Nennspannung der Pumpe bestimmen
Duenger_Pumpe = MOSFET_Steuerung(pin=17,tastgrad=39)

try:
    Duenger_Pumpe.start()
    # Zeitdelay für Pumpenlaufzeit
    time.sleep(10)
finally: # "finally" ermöglicht das Stoppen der Pumpe auch wenn das Programm vor Ablauf der Pumpenlaufzeit gestoppt wird
    Duenger_Pumpe.stop()
    Duenger_Pumpe.cleanup()