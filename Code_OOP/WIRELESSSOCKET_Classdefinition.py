import RPi.GPIO as GPIO
from gpiozero import LED
import time
import datetime
from PARAMETERS_Definition import parameters

# Definition einer Klasse für Objekte welche über Funksteckdosen angesteuert werden
class WIRELESSSOCKET_control:

    # Definition von Klassenattributen welche für alle Objekte der Klasse gelten
    ON = LED(parameters.wirelesssocket_pin_on) # BCM-Nummer 27 = Pin 13 als Impulssignal für Relais on
    OFF = LED(parameters.wirelesssocket_pin_off) # BCM-Nummer 22 = Pin 15 als Impulssignal für Relais off
    schaltzeit = 0.2 # Wartezeit für zuverlässige Schaltung der Relais

    def __init__(self, pin):
        self.pin = pin # Pin zur Ansteuerung des Relais
        self.LED = LED(self.pin)
        self.status = False # Der Status gibt an ob das Objekt an der Fnksteckdose an oder ausgeschaltet ist, zu Beginn ausgeschaltet
        self.statusbeforemeasurement = False # Hilfsparameter zum Rückschalten der Objekte nach Messungen
        self.setup()

    # Funktion wird ebenfalls bei Initialisierung ausgeführt um Relais zu Beginn auszuschalten
    # Achtung "on" bedeutet hier "off"
    def setup(self):
        self.LED.off()
        WIRELESSSOCKET_control.ON.off()
        WIRELESSSOCKET_control.OFF.off()

    # Definition von Klassenmethoden zum Ein- und Ausschalten der Steckdosen
    def on(self):
        self.LED.on()
        WIRELESSSOCKET_control.ON.on()
        time.sleep(WIRELESSSOCKET_control.schaltzeit)
        self.LED.off()
        WIRELESSSOCKET_control.ON.off()
        self.status = True # Ändern des Status des Objekts zu Eingeschaltet

    def off(self):
        self.LED.on()
        WIRELESSSOCKET_control.OFF.on()
        time.sleep(WIRELESSSOCKET_control.schaltzeit)
        self.LED.off()
        WIRELESSSOCKET_control.OFF.off()
        self.status = False # Ändern des Status des Objekts zu Ausgeschaltet
