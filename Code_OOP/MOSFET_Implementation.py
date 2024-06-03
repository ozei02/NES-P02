# Erforderliche Bibliotheken importieren
import time
# Importieren der MOSFET_Steuerung Klasse aus MOSFET_Classdefinition um in diesem Skript ein Objekt erstellen zu können
from MOSFET_Classdefinition import MOSFET_control

# Instanziieren der Düngerpumpe als Objekt der MOSFET Klasse
# Pin je nach Anschluss an den Raspberry anpassen
# Tastgrad je nach Netzteil und Nennspannung der Pumpe bestimmen
# Startzeit beschreibt im Fall der Düngepumpe die Laufzeit bis die Leitungen komplett mit Düngemittel befüllt sind
Duenger_Pumpe = MOSFET_control(pin=17,tastgrad=39, startuptime=30)

# Verwendung von try und finally um sicherzustellen dass die Pumpe stoppt sollte während dem Pumpenprogramm ein Fehler auftreten
try:
    Duenger_Pumpe.startup()
    Duenger_Pumpe.start()
    # Zeitdelay für Pumpenlaufzeit
    time.sleep(10)
finally: 
    Duenger_Pumpe.stop()
    Duenger_Pumpe.cleanup()