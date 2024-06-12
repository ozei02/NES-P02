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

    def __init__(self, pin, on_time, off_time):
        self.pin = pin # Pin zur Ansteuerung des Relais
        self.LED = LED(self.pin)
        self.on_time = on_time # Definition der Zeit die das Objekt eingeschaltet bleibt
        self.off_time = off_time # Definition der Zeit die das Objekt ausgeschaltet bleibt
        self.status = False # Der Status gibt an ob das Objekt an der Fnksteckdose an oder ausgeschaltet ist, zu Beginn ausgeschaltet
        self.statusbeforemeasurement = False # Hilfsparameter zum Rückschalten der Objekte nach Messungen
        self.setup()

    # Funktion wird ebenfalls bei Initialisierung ausgeführt um Relais zu Beginn auszuschalten
    # Achtung "on" bedeutet hier "off"
    def setup(self):
        self.LED.on()
        WIRELESSSOCKET_control.ON.on()
        WIRELESSSOCKET_control.OFF.on()

    # Definition von Klassenmethoden zum Ein- und Ausschalten der Steckdosen
    def on(self):
        self.LED.off()
        WIRELESSSOCKET_control.ON.off()
        time.sleep(WIRELESSSOCKET_control.schaltzeit)
        self.LED.on()
        WIRELESSSOCKET_control.ON.on()
        self.status = True # Ändern des Status des Objekts zu Eingeschaltet
        # Codeblock zur Ausgabe der Änderung zum eingeschalteten Zustand im Command Fenster
        now = datetime.datetime.now() # aktuelles Datum und Zeit
        date_time = now.strftime("%Y-%m-%d, %H:%M:%S") # Zeitstempel zu dem das Objekt geschaltet wird
        Object_Name = self.__class__.__name__ # Name des Klassenobjekts
        print(f"{date_time}: {Object_Name} zeitgesteuert eingeschaltet nach {(self.off_time)/60:5.1f} Minuten")
    
    # Methode zum Einschalten bei Messungen
    def on_for_measurement(self):
        self.LED.off()
        WIRELESSSOCKET_control.ON.off()
        time.sleep(WIRELESSSOCKET_control.schaltzeit)
        self.LED.on()
        WIRELESSSOCKET_control.ON.on()
        self.status = True # Ändern des Status des Objekts zu Eingeschaltet
        # Codeblock zur Ausgabe der Änderung zum eingeschalteten Zustand im Command Fenster
        now = datetime.datetime.now() # aktuelles Datum und Zeit
        date_time = now.strftime("%Y-%m-%d, %H:%M:%S") # Zeitstempel zu dem das Objekt geschaltet wird
        Object_Name = self.__class__.__name__ # Name des Klassenobjekts
        print(f"{date_time}: {Object_Name} für oder nach Messung eingeschaltet")

    def off(self):
        self.LED.off()
        WIRELESSSOCKET_control.OFF.off()
        time.sleep(WIRELESSSOCKET_control.schaltzeit)
        self.LED.on()
        WIRELESSSOCKET_control.OFF.on()
        self.status = False # Ändern des Status des Objekts zu Ausgeschaltet
        # Codeblock zur Ausgabe der Änderung zum ausgeschalteten Zustand im Command Fenster
        now = datetime.datetime.now() # aktuelles Datum und Zeit
        date_time = now.strftime("%Y-%m-%d, %H:%M:%S") # Zeitstempel zu dem das Objekt geschaltet wird
        Object_Name = self.__class__.__name__ # Name des Klassenobjekts
        print(f"{date_time}: {Object_Name} zeitgesteuert ausgeschaltet nach {(self.on_time)/60:5.1f} Minuten")

    # Methode zum Ausschalten bei Messungen
    def off_for_measurement(self):
        self.LED.off()
        WIRELESSSOCKET_control.OFF.off()
        time.sleep(WIRELESSSOCKET_control.schaltzeit)
        self.LED.on()
        WIRELESSSOCKET_control.OFF.on()
        self.status = False # Ändern des Status des Objekts zu Ausgeschaltet
        # Codeblock zur Ausgabe der Änderung zum ausgeschalteten Zustand im Command Fenster
        now = datetime.datetime.now() # aktuelles Datum und Zeit
        date_time = now.strftime("%Y-%m-%d, %H:%M:%S") # Zeitstempel zu dem das Objekt geschaltet wird
        Object_Name = self.__class__.__name__ # Name des Klassenobjekts
        print(f"{date_time}: {Object_Name} für oder nach Messung ausgeschaltet")