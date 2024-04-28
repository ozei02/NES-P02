#coding: utf8
# Erforderliche Bibliotheken importieren
import RPi.GPIO as GPIO
import time

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

uhrzeigersinn.ChangeDutyCycle(100)
time.sleep(2)
uhrzeigersinn.stop()