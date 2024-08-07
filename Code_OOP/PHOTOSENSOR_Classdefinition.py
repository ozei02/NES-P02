from adafruit_as7341 import AS7341 # Ermöglicht Interaktion mit dem AS7341 Fotosensor
import board

class PHOTOSENSOR_reading:

    # Definition von Klassenattributen welche für alle Objekte der Klasse gelten
    i2c = board.I2C()  # verwendet board.SCL und board.SDA
    sensor = AS7341(i2c)

    verhaeltnis_reaktor_zu_probe = 0.35635681 # Verhältnis der Reflexionswerte zwischen Reaktor und Probe
    sensor.led_current = 5 # Setzt den LED-Strom auf 5mA
    channels = ['415nm', '445nm', '480nm', '515nm', '555nm', '590nm', '630nm', '680nm', 'Clear', 'NIR']
    colors = ['violet', 'indigo', 'blue', 'cyan', 'green', 'yellow', 'orange', 'red', 'grey', 'black']
    messmodus = "Reactor"


    def __init__(self):
        self.algae_concentration = 0
        self.value = 0

    def read_channels(self):
        self.channel_data = [
                    PHOTOSENSOR_reading.sensor.channel_415nm, PHOTOSENSOR_reading.sensor.channel_445nm, PHOTOSENSOR_reading.sensor.channel_480nm,
                    PHOTOSENSOR_reading.sensor.channel_515nm, PHOTOSENSOR_reading.sensor.channel_555nm, PHOTOSENSOR_reading.sensor.channel_590nm,
                    PHOTOSENSOR_reading.sensor.channel_630nm, PHOTOSENSOR_reading.sensor.channel_680nm, PHOTOSENSOR_reading.sensor.channel_clear,
                    PHOTOSENSOR_reading.sensor.channel_nir
                    ]

    # Liest den Sensorwert bei clear. Passt den Wert an, wenn im "Reaktor"-Modus
    def get_algae_concentration(self, adjust_for_mode=True):
        self.read_channels()
        raw_value = PHOTOSENSOR_reading.sensor.channel_clear
        if adjust_for_mode:
            if PHOTOSENSOR_reading.messmodus == "Reactor":
                adjusted_value = raw_value / PHOTOSENSOR_reading.verhaeltnis_reaktor_zu_probe
                print(f"Angepasster Wert (Reaktor): {adjusted_value}")  # Debugging-Ausgabe
                self.value = adjusted_value
            elif PHOTOSENSOR_reading.messmodus == "Probenbox":
                # Optional: Hier könnte eine Anpassung für die Probenbox erfolgen
                print(f"Angepasster Wert (Probenbox): {raw_value}")  # Debugging-Ausgabe
                self.value = raw_value
        else:
            self.value = raw_value
        self.algae_concentration = self.calculate_algae_concentration()
    
    # Berechnet die Algenkonzentration basierend auf dem Sensorwert
    def calculate_algae_concentration(self):
        m = -1.0500363424809021e-06
        b = 39040.888573888915
        algae_concentration = (self.value - b) / m
        return algae_concentration
    