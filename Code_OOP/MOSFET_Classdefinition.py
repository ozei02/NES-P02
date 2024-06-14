import RPi.GPIO as GPIO
import tkinter as tk
import time
from PARAMETERS_Definition import parameters

# Definition einer Klasse für Objekte welche mit einem MOSFET angesteuert werden
class MOSFET_control:
    # Die __init__ Methode ist der Konstruktor der Klasse, wird also verwendet um neue Objekte hinzuzufügen
    def __init__(self, pin, dutycycle, startuptime, actiontime):
        self.pin = pin
        self.dutycycle = dutycycle
        self.startuptime = startuptime
        self.actiontime = actiontime
        self.flooded = False # Parameter welcher auf True gesetzt wird sobald der Nutzer bestätigt dass die Leitungen der Pumpe geflutet sind
        self.setup()
    
    # Setup des Output Pins und der Pulsweitenmodulation (Wird bei der Initialisierung mit durchgeführt)
    def setup(self):
        GPIO.setmode(GPIO.BCM) # Konvention der Pinnummerierung (hier BCM)
        GPIO.setwarnings(False) # Warnungen, die das Ausführen des Programms verhindern, wenn Ausgang bereits als OUT deklariert wurde ignorieren
        GPIO.setup(self.pin, GPIO.OUT) # Definition des Pins als Output-Pin
        self.pwm = GPIO.PWM(self.pin, 50) # PWM mit 50Hz Frequenz initialisieren
        self.pwm.start(0) # PWM mit 0% Tastgrad starten
    
    # Methode welche ausgeführt wird sobald der Button zum pumpstartup geklickt wird
    def on_button_click_pumpstartup(self):
        self.button_pumpstartup_clicked = True
        self.pumpstartup.destroy() # Schließt das Pop-up-Fenster
        self.pwm.ChangeDutyCycle(self.dutycycle) # Starten der Pumpe
        print(f"Pumpe wird für {self.startuptime} Sekunden gestartet um Ansaug- und Auslaufschlauch zu durchfluten. Bitte warten...")
        time.sleep(self.startuptime) # Startup Zeit der Pumpe
        # Stoppen der Pumpe
        self.off()
        self.startup()

    # Methode welche als Anlaufprogramm für die Pumpe fungiert um eine komplette Durchflutung der Schläuche mit Düngemittel zu Beginn des Versuchs zu realisieren
    def startup(self):
        # Initialisierung des Pup-up-Fensters
        self.pumpstartup = tk.Tk()
        self.pumpstartup.title("Startprozedur der Düngepumpe")
        # Hinzufügen von Text
        self.label_instruction = tk.Label(self.pumpstartup, text="Bitte sicherstellen, dass die Leitungen der Pumpe vollständig gefüllt sind.")
        self.label_instruction.pack(pady=10)
        # Erstellen des Buttons zum Pumpe starten
        self.button_pumpstartup = tk.Button(self.pumpstartup, text="Pumpe durchfluten", command=self.on_button_click_pumpstartup) 
        self.button_pumpstartup.pack(pady=10)
        # Erstellen des Buttons zum Hauptprogramm starten
        self.button_mainstartup = tk.Button(self.pumpstartup, text="Hauptprogramm starten", command=self.on_button_click_mainstartup) 
        self.button_mainstartup.pack(pady=10)        
        # Variable um den Button-Klick zu verfolgen
        self.button_pumpstartup_clicked = False
        self.button_mainstartup_clicked = False
        # Zeige das Pop-up-Fenster
        self.pumpstartup.mainloop()

    # Methode welche ausgeführt wird sobald die durchfluteten Leitungen verifiziert wurden
    def on_button_click_mainstartup(self):
        self.button_mainstartup_clicked = True
        self.flooded = True
        self.pumpstartup.destroy() # Schließt das Pop-up-Fenster
        print(f"Durchflutete Leitungen der Pumpe verifiziert. Hauptprogramm wird gestartet")        

    # Start der Pulsweitenmodulation mit gewünschtem Tastgrad
    def on(self):
        self.pwm.ChangeDutyCycle(self.dutycycle)
        time.sleep(self.actiontime)
        self.off()
        print("Düngung durchgeführt")

    # Ende der Pulsweitenmodulation
    def off(self):
        self.pwm.ChangeDutyCycle(0)

    # GPIO Cleanup und stoppen der PWM
    def cleanup(self):
        self.pwm.stop()
        GPIO.cleanup()
