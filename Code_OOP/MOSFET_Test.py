# Erforderliche Bibliotheken importieren
import time
# Importieren der MOSFET_Steuerung Klasse aus MOSFET_Classdefinition um in diesem Skript ein Objekt erstellen zu können
from MOSFET_Classdefinition import MOSFET_control
from PARAMETERS_Definition import parameters

# Instanziieren der Düngerpumpe als Objekt der MOSFET Klasse
# Pin je nach Anschluss an den Raspberry anpassen
# Tastgrad je nach Netzteil und Nennspannung der Pumpe bestimmen
# Startzeit beschreibt im Fall der Düngepumpe die Laufzeit bis die Leitungen komplett mit Düngemittel befüllt sind
fertilizer_pump = MOSFET_control(pin=parameters.fertilizerpump_pin,dutycycle=parameters.fertilizerpump_dutycycle, startuptime=parameters.fertilizerpump_startuptime, actiontime=parameters.fertilizerpump_actiontime)

# Verwendung von try und finally um sicherzustellen dass die Pumpe stoppt sollte während dem Pumpenprogramm ein Fehler auftreten
try:
    fertilizer_pump.startup()
    # Start des eigentlichen Programms
    if fertilizer_pump.flooded == True:
        fertilizer_pump.on()

finally: 
    fertilizer_pump.off()
    fertilizer_pump.cleanup()