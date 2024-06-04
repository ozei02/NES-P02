import RPi.GPIO as GPIO
import tkinter as tk
import time

# Definition einer Klasse für Objekte welche mit einem MOSFET angesteuert werden
class MOSFET_control:
    # Die __init__ Methode ist der Konstruktor der Klasse, wird also verwendet um neue Objekte hinzuzufügen
    def __init__(self, pin, dutycycle, startuptime):
        self.pin = pin
        self.dutycycle = dutycycle
        self.startuptime = startuptime
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
        self.stop
        self.verification

    # Methode welche als Anlaufprogramm für die Pumpe fungiert um eine komplette Durchflutung der Schläuche mit Düngemittel zu Beginn des Versuchs zu realisieren
    def startup(self):
        # Initialisierung des Pup-up-Fensters
        self.pumpstartup = tk.Tk()
        self.pumpstartup.title("Sicherstellen von vollständig durchfluteten Leitungen der Düngepumpe")
        # Erstellen des Buttons
        self.button_pumpstartup = tk.Button(self.pumpstartup, text="Start", command=self.on_button_click_pumpstartup) 
        self.button_pumpstartup.pack(pady=20)
        # Variable um den Button-Klick zu verfolgen
        self.button_pumpstartup_clicked = False
        # Zeige das Pop-up-Fenster
        self.pumpstartup.mainloop()

    # Methode welche ausgeführt wird sobald die durchfluteten Leitungen verifiziert wurden
    def on_button_click_pumpverification(self):
        self.button_pumpverification_clicked = True
        self.flooded = True
        self.pumpverification.destroy() # Schließt das Pop-up-Fenster
        print(f"Durchflutete Leitungen der Pumpe verifiziert. Hauptprogramm wird gestartet")

    # Methode für das Pop-up welches nach dem startup als Verifikation der durchfluteten Leitungen dient
    def verification(self):
        # Initialisierung des Pup-up-Fensters
        self.pumpverification = tk.Tk()
        self.pumpverification.title("Sind die Leitungen der Düngepumpe vollständig gefüllt?")
        # Erstellen des Buttons
        self.button_pumpverification = tk.Button(self.pumpverification, text="Verifizieren: Hauptprogramm starten", command=self.on_button_click_pumpverification) 
        self.button_pumpverification.pack(pady=20)
        # Variable um den Button-Klick zu verfolgen
        self.button_pumpverification_clicked = False
        # Zeige das Pop-up-Fenster
        self.pumpverification.mainloop()        

    # Start der Pulsweitenmodulation mit gewünschtem Tastgrad
    def start(self):
        self.pwm.ChangeDutyCycle(self.dutycycle)

    # Ende der Pulsweitenmodulation
    def stop(self):
        self.pwm.ChangeDutyCycle(0)

    # GPIO Cleanup und stoppen der PWM
    def cleanup(self):
        self.pwm.stop()
        GPIO.cleanup()
