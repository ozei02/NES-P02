import RPi.GPIO as GPIO
import time
from datetime import datetime
import keyboard

TRIG = 23
ECHO = 18
Pout = 17
anzahl_messwerte = 5
distances = []

# Xo = 0                             # Einführung x0 als Startwert
dX = 50                            # delta x in cm 
# dXa = 0         	               # Aktualwert xa ab nivilierung
Pumpensteuerung = GPIO.PWM(Pout, 50)
Pumpensteuerung.start(0)

def setup():
    GPIO.setmode(GPIO.BCM)         # von Board auf BCM geändert
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
    return during * 340 / 2 * 1000

def get_average_distances():
    global Xo, dXa
    if len(distances) < anzahl_messwerte:
        return None
    
    elif len(distances) == anzahl_messwerte:                         # nach ersten 5 Messungen wird initial Xo aus gesetzt
        last_mesurements = distances[-anzahl_messwerte:]
        average_distance = sum(last_mesurements) / anzahl_messwerte
        return average_distance
    else:
        last_mesurements = distances[-anzahl_messwerte:]
        average_distance = sum(last_mesurements) / anzahl_messwerte
        return average_distance

def loop():
    global Pumpensteuerung, dX
    while True:
        dis = distance()
        print ('Distance: %.2f mm' % dis)
        distances.append(dis)
        if len(distances) == anzahl_messwerte:
            Xo = get_average_distances()
            Pumpensteuerung.ChangeDutyCycle(100)
        if len(distances) >= anzahl_messwerte:
            dXa = get_average_distances() - Xo
            average_distance = get_average_distances()
            if average_distance is not None:
                print('average Distance (last 5 measurements): %.2f mm' % average_distance)
            if dXa >= dX:
                time.sleep(100)
        time.sleep(0.5)                                           #Messintervall

def destroy():
    GPIO.cleanup()


#Skript
setup()
loop()


