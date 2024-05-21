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
GPIO.setup(17, GPIO.OUT)    # Verbraucher 1 (graue Kabel)
GPIO.setup(27, GPIO.OUT)    # Verbraucher 2 (orange Kabel)

# PWM= PulsWeitenModulation für beide Verbraucher mit Frequenz festlegen
Verbraucher1 = GPIO.PWM(17, 50)
Verbraucher2 = GPIO.PWM(27, 50)

# PWM mit Tastgrad 0% initialisieren; Wie viel % der Periode angeschaltet sind 
Verbraucher1.start(0)
Verbraucher2.start(0)

# Start von Verbraucher1 mit gewünschtem Tastgrad für x Sekunden
Tastgrad = 100
LaufzeitVerbraucher1 = 5
Verbraucher1.ChangeDutyCycle(Tastgrad)
time.sleep(LaufzeitVerbraucher1)
Verbraucher1.stop()

# Start von Verbraucher2 mit gewünschtem Tastgrad für x Sekunden
Tastgrad = 100
LaufzeitVerbraucher2 = 5
Verbraucher2.ChangeDutyCycle(Tastgrad)
time.sleep(LaufzeitVerbraucher2)
Verbraucher2.stop()

# Start beider Verbraucher gleichzeitig mit gewünschtem Tastgrad für x Sekunden
Tastgrad = 100
LaufzeitGleichzeitig = 5
Verbraucher1.ChangeDutyCycle(Tastgrad)
Verbraucher2.ChangeDutyCycle(Tastgrad)
time.sleep(LaufzeitGleichzeitig)
Verbraucher1.stop()
Verbraucher2.stop()