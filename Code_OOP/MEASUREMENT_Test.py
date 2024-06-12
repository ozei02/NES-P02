from MEASUREMENT_Functions import measurement_bright, measurement_dark
from WIRELESSSOCKET_Classdefinition import WIRELESSSOCKET_control
from PARAMETERS_Definition import parameters
import time

# Messungen mit Ausschalten der Luftpumpe

time.sleep(20)

measurement_bright()
measurement_dark()

time.sleep(20)

# Messungen ohne Ausschalten der Luftpumpe

measurement_bright()
measurement_dark()