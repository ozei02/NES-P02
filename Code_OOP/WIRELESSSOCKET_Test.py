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

# Starten des Timers für die Ausführungen
timer = time()

# Hauptschleife
while timer <= test_time:

    if (lamps.status == False) and (timer-lasttime_lamps_off >= lamps_off_time):
        lamps.on()
        lasttime_lamps_on = timer

    if (lamps.status == True) and (timer-lasttime_lamps_on >= lamps_on_time):
        lamps.off()
        lasttime_lamps_off = timer

    if (airpump.status == False) and (timer-lasttime_airpump_off >= airpump_off_time):
        airpump.on()
        lasttime_airpump_on = timer

    if (airpump.status == True) and (timer-lasttime_airpump_on >= airpump_on_time):
        airpump.off()
        lasttime_airpump_off = timer