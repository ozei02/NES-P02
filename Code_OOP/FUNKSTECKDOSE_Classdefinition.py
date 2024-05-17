import RPi.GPIO as GPIO
from gpiozero import LED
import time

# Definition einer Klasse für Objekte welche über Funksteckdosen angesteuert werden
class FUNKSTECKDOSE_Steuerung:

    # Definition von Klassenattributen welche für alle Objekte der Klasse gelten
    ON = LED(27) # BCM-Nummer 27 = Pin 13 als Impulssignal für Relais on
    OFF = LED(22) # BCM-Nummer 22 = Pin 15 als Impulssignal für Relais off
    schaltzeit = 0.2 # Wartezeit für zuverlässige Schaltung der Relais

    def __init__(self, pin):
        self.pin = pin # Pin zur Ansteuerung des Relais
        self.LED = LED(self.pin)
        self.status = False # Der Status gibt an ob das Objekt an der Fnksteckdose an oder ausgeschaltet ist, zu Beginn ausgeschaltet
        self.setup()

    # Funktion wird ebenfalls bei Initialisierung ausgeführt um Relais zu Beginn auszuschalten
    # Achtung "on" bedeutet hier "off"
    def setup(self):
        self.LED.on()
        FUNKSTECKDOSE_Steuerung.ON.on()
        FUNKSTECKDOSE_Steuerung.OFF.on()

    # Definition von Klassenmethoden zu Ein- und Ausschalten der Steckdosen
    def EIN(self):
        self.LED.off()
        FUNKSTECKDOSE_Steuerung.ON.off()
        time.sleep(FUNKSTECKDOSE_Steuerung.schaltzeit)
        self.LED.on()
        FUNKSTECKDOSE_Steuerung.ON.off()
        self.status = True # Ändern des Status des Objekts zu Eingeschaltet
    
    def AUS(self):
        self.LED.off()
        FUNKSTECKDOSE_Steuerung.OFF.off()
        time.sleep(FUNKSTECKDOSE_Steuerung.schaltzeit)
        self.LED.on()
        FUNKSTECKDOSE_Steuerung.OFF.on()
        self.status = False # Ändern des Status des Objekts zu Ausgeschaltet
