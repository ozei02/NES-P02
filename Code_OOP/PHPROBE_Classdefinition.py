from sklearn.linear_model import LinearRegression # Dies deutet darauf hin, dass das Programm eine lineare Regressionsanalyse mit der scikit-learn-Bibliothek durchführen möchte.
import numpy as np # Stellt Funktionen zum rechnen in Matrizen usw. bereit
import adafruit_ads1x15.ads1115 as ADS # Ermöglicht auf den ADS1115 Analog-Digital-Wandler (ADC) zuzugreifen (Messen von physikalischen Größen wie Spannung, Strom, Temperatur, ...)
import board # Ermöglicht das Arbeiten mit GPIOs auf dem Raspberry Pi (Ermöglicht Interaktion mit benutzerfreunlicherer API statt direkte Interaktion mit Hardware Pins)
import busio # Ermöglicht vereinfachte Kommunikation über serielle Busse wie I2C oder SPI
from adafruit_ads1x15.analog_in import AnalogIn     # AnalogIn Klasse wird verwendet um ein analoges Einganssignal des ADCs zu repräsentieren und in digitale Werte umzuwandeln
class PHPROBE_control:
    
    # Ansprechen der PH-Sonde
    i2c = busio.I2C(board.SCL, board.SDA) # Ansprechen über Pin SCL (GPIO 3) und Pin SDA (GPIO 2)
    ads = ADS.ADS1115(i2c) # Zugriff auf Analog-Digital-Wandler (ADC) um analoges Spannungssignal der PH-Sonde in digitales Signal umzuwandeln
    
    # Kalibrierwerte der pH-Sonde mit Referenzlösungen gemessen
    x = np.array([2.016, 1.515, 1.119]).reshape((-1, 1))	# gemessene Spannungswerte für Kalibrierlösungen
    y = np.array([4.0, 6.88, 9.23]) # pH-Werte der Kalibrierlösungen
    pHmodel = LinearRegression().fit(x, y) # lineares Kalibriermodell pH-Sonde

    def __init__(self):
        self.chan = AnalogIn(PHPROBE_control.ads, ADS.P0) # Initialisiert den analogen Eingangskanal am ADC
   
    def measure(self):
        # Messwert als Spannung
        spannung = self.chan.voltage
        # Messwert umgerechnet zu pH-Wert
        pH = spannung * PHPROBE_control.pHmodel.coef_[0] + PHPROBE_control.pHmodel.intercept_
        return pH

    