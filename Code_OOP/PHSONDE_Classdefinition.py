from sklearn.linear_model import LinearRegression # Dies deutet darauf hin, dass das Programm eine lineare Regressionsanalyse mit der scikit-learn-Bibliothek durchführen möchte.
import numpy as np # Stellt Funktionen zum rechnen in Matrizen usw. bereit
import adafruit_ads1x15.ads1115 as ADS # Ermöglicht auf den ADS1115 Analog-Digital-Wandler (ADC) zuzugreifen (Messen von physikalischen Größen wie Spannung, Strom, Temperatur, ...)

class PHSONDE_control:

    # Kalibrierwerte der pH-Sonde mit Referenzlösungen gemessen
    x = np.array([2.016, 1.515, 1.119]).reshape((-1, 1))	# gemessene Spannungswerte für Kalibrierlösungen
    y = np.array([4.0, 6.88, 9.23]) # pH-Werte der Kalibrierlösungen
    pHmodel = LinearRegression().fit(x, y) # lineares Kalibriermodell pH-Sonde