import RPi.GPIO as GPIO
import time
from datetime import datetime



TRIG = 16
ECHO = 18
anzahl_messwerte = 5
distances = []

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

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
    else:
        last_mesurements = distances[-anzahl_messwerte:]
        average_distance = sum(last_mesurements) / anzahl_messwerte
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
        time.sleep(1)


def destroy():
    GPIO.cleanup()

if __name__ == "__main__":
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()

#### Pumpensteuerung

import RPi.GPIO as GPIO
import time
 
# Konvention für Pinnummerierung festlegen (BCM bzw. Board)
GPIO.setmode(GPIO.BCM)
# Warnungen, die das Ausführen des Programms verhindern, wenn
# Ausgang bereits als OUT deklariert wurde ignorieren
GPIO.setwarnings(False)
# Pins als Ausgänge deklarieren
GPIO.setup(21, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)
 
# PWM für Richtungen mit Frequenz festlegen
uhrzeigersinn = GPIO.PWM(21, 50)
gegen_uhrzeigersinn = GPIO.PWM(25, 50)
# PWM mit Tastgrad 0% initialisieren
uhrzeigersinn.start(0)
gegen_uhrzeigersinn.start(0)
 
uhrzeigersinn.ChangeDutyCycle(100)
time.sleep(2)
uhrzeigersinn.stop()
gegen_uhrzeigersinn.ChangeDutyCycle(100)
time.sleep(2)
gegen_uhrzeigersinn.stop()