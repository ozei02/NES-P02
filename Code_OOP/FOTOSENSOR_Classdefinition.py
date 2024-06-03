from adafruit_as7341 import AS7341 # Ermöglicht Interaktion mit dem AS7341 Fotosensor

class FOTOSENSOR_Messung:

    # Definition von Klassenattributen welche für alle Objekte der Klasse gelten
    verhaeltnis_reaktor_zu_probe = 0.35635681 # Verhältnis der Reflexionswerte zwischen Reaktor und Probe
    led_current = 5 # Setzt den LED-Strom auf 5mA
    channels = ['415nm', '445nm', '480nm', '515nm', '555nm', '590nm', '630nm', '680nm', 'Clear', 'NIR']
    colors = ['violet', 'indigo', 'blue', 'cyan', 'green', 'yellow', 'orange', 'red', 'grey', 'black']


    def __init__(self):
        pass

    def messung_bright(self, lamp):
