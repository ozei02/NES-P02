import RPi.GPIO as GPIO
import time
import os.path
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

def save_data(data):
    if not os.path.isfile("distanzdaten"):
        open("distanzdaten.txt", "w").close()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open("distanzdaten.txt", "a") as file:
            file.write("%s - %.2f mm/n" % (now, data))
            file.flush()
    except IOError as e:
        print("fehler beim schreiben der datei", e)

def destroy():
    GPIO.cleanup()

if __name__ == "__main__":
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
