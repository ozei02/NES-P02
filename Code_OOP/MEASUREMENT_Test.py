from MEASUREMENT_Functions import measurement_bright, measurement_dark
from WIRELESSSOCKET_Classdefinition import WIRELESSSOCKET_control
from PARAMETERS_Definition import parameters
import time

lamps = WIRELESSSOCKET_control(pin=17, on_time=parameters.lamps_on_time, off_time=parameters.lamps_off_time)
airpump = WIRELESSSOCKET_control(pin=18, on_time=parameters.airpump_on_time, off_time=parameters.airpump_off_time)

try:
    # Messungen mit Ausschalten der Luftpumpe
    lamps.on()
    airpump.on()

    time.sleep(20)

    measurement_bright()
    measurement_dark()

    time.sleep(20)

    # Messungen ohne Ausschalten der Luftpumpe
    lamps.off()
    airpump.off()

    measurement_bright()
    measurement_dark()
finally:
    lamps.off()
    airpump.off()