from WIRELESSSOCKET_Classdefinition import WIRELESSSOCKET_control     
import time

# Initialparameter der Objekte mit Funksteckdose
lasttime_lamps_on = 0
lasttime_lamps_off = 0
lasttime_airpump_on = 0
lasttime_airpump_off = 0

# Testparameter
lamps_on_time = 15
lamps_off_time = 15
airpump_on_time = 30
airpump_off_time = 30
test_time = 2*60

# Initialisieren der Klassenobjekte
lamps = WIRELESSSOCKET_control(pin=17, on_time=lamps_on_time, off_time=lamps_off_time)
airpump = WIRELESSSOCKET_control(pin=18, on_time=airpump_on_time, off_time=airpump_off_time)

lamps.on()
airpump.on()

time.sleep(10)

lamps.off()
airpump.off()