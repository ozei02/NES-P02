#coding: utf8
# Erforderliche Bibliotheken importieren
import RPi.GPIO as GPIO
import time
import keyboard

def on_key_press(key):
    if key.name == 'esc':  # Hier wird überprüft, ob die Escape-Taste gedrückt wurde
        print("Programm wird beendet...")
        # Hier kannst du Aufräumarbeiten oder weitere Aktionen vor dem Beenden ausführen
        uhrzeigersinn.stop()
        Prog_Abbruchzeit = time.time()
        # Berechnen der Programmzeit aus Startzeit und Endzeit
        Prog_Laufzeit = Prog_Abbruchzeit - Prog_Startzeit 
        # Ausgeben der gewünschten Messdaten
        print(f"Tastgrad: {Tastgrad}")
        print(f"Laufzeit für 100ml: {Prog_Laufzeit}")
        keyboard.unhook_all()  # Alle Tastaturhaken entfernen, um das Programm zu beenden
        quit()  # Programm beenden

# Konvention für Pinnummerierung festlegen (BCM bzw. Board)
GPIO.setmode(GPIO.BCM)
# Warnungen, die das Ausführen des Programms verhindern, wenn
# Ausgang bereits als OUT deklariert wurde ignorieren
GPIO.setwarnings(False)
# Pins als Ausgänge deklarieren
GPIO.setup(17, GPIO.OUT)

# PWM für Richtungen mit Frequenz festlegen
uhrzeigersinn = GPIO.PWM(17, 50)

# PWM mit Tastgrad 0% initialisieren
uhrzeigersinn.start(0)

# Start der Pumpe mit gewünschtem Tastgrad
Tastgrad = 100
uhrzeigersinn.ChangeDutyCycle(Tastgrad)

#Zeit zum Programmstart
Prog_Startzeit = time.time()

# Ausführen der oben definierten on_key_press Funktion zum Programmabbruch und Auswertung beim drücken von "esc"
keyboard.on_press(on_key_press)
