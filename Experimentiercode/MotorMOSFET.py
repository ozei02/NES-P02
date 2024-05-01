#coding: utf8
# Erforderliche Bibliotheken importieren
import RPi.GPIO as GPIO  #für engl. General Purpose Input/Output, wörtlich Allzweckeingabe/-ausgabe
import time

# Konvention für Pinnummerierung festlegen (BCM bzw. Board)
GPIO.setmode(GPIO.BCM)
# Warnungen, die das Ausführen des Programms verhindern, wenn
# Ausgang bereits als OUT deklariert wurde ignorieren
GPIO.setwarnings(False)
# Pins als Ausgänge deklarieren
GPIO.setup(17, GPIO.OUT)

# PWM= PulsWeitenModulation für Richtungen mit Frequenz festlegen
uhrzeigersinn = GPIO.PWM(17, 50)

# PWM mit Tastgrad 0% initialisieren; Wie viel % der Periode angeschaltet sind 
uhrzeigersinn.start(0)

#Schleife zur PWM
Tastgrad = 0
while Tastgrad <= 100:
    uhrzeigersinn.ChangeDutyCycle(Tastgrad)  #ChangeDutyCycle funktion zum änderung der Tastrate
    time.sleep(2)                            #stopt für zwei sec den code
    Tastgrad = Tastgrad + 5                  #alle 2 sec 5% höher
uhrzeigersinn.stop()