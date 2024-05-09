import RPi.GPIO as GPIO
import time
from datetime import datetime
import keyboard



TRIG = 23
ECHO = 18
Pout = 17
anzahl_messwerte = 5
distances = []

Xo = 0              # Einführung x0 als Startwert
dX = 0.5            # delta x in cm 
dXa = ()         	# Aktualwert xa ab nivilierung

def setup():
    GPIO.setmode(GPIO.BCM)      # von Board auf BCM geändert
    GPIO.setwarnings(False)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.setup(Pout, GPIO.OUT)

def distance():
    GPIO.output(TRIG, 0)
    time.sleep(0.000002)
    GPIO.output(TRIG, 1)
    time.sleep(0.00001)
    GPIO.output(TRIG, 0)

    while GPIO.input(ECHO) == 0:
        pass
    start_time = time.time()
    while GPIO.input(ECHO) == 1:
        pass
    end_time = time.time()
    during = end_time - start_time
    return during * 340 / 2 * 100

def get_average_distances():
    if len(distances) < anzahl_messwerte:
        return None
    
    elif len(distances) = anzahl_messwerte:                         # nach ersten 5 Messungen wird initial Xo aus gesetzt
        last_mesurements = distances[-anzahl_messwerte:]
        average_distance = sum(last_mesurements) / anzahl_messwerte
        Xo = average_distance                                       # Xo
        return average_distance
    else:
        last_mesurements = distances[-anzahl_messwerte:]
        average_distance = sum(last_mesurements) / anzahl_messwerte
        dXa = Xo - average_distance                                  # Aktualwer Xa aus durchschnittlicher Änderung
        return average_distance

def loop():
    while True:
        dis = distance()
        print ('Distance: %.2f mm' % dis)
        distances.append(dis)
        if len(distances) >= anzahl_messwerte:
            average_distance = get_average_distances()
            if average_distance is not None:
                print('average Distance (last 5 measurements): %.2f mm' % average_distance)
        time.sleep(0.5)                                           #Messinertvall
def Motor(pwm,tg):
    Pumpensteuerung = GPIO.PWM(Pout, pwm)
    Pumpensteuerung.start(0)
    Pumpensteuerung.ChangeDutyCycle(tg)
    if dXa >= dX: 
        Pumpensteuerung.stop()
def destroy():
    GPIO.cleanup()


setup()
loop()
Motor(50,100)



#### Pumpensteuerung

# PWM= PulsWeitenModulation für Richtungen mit Frequenz festlegen


# PWM mit Tastgrad 0% initialisieren; Wie viel % der Periode angeschaltet sind 


# Start der Pumpe mit gewünschtem Tastgrad


#Zeit zum Programmstart
# Prog_Startzeit = time.time()

