from WIRELESSSOCKET_Classdefinition import WIRELESSSOCKET_control
import time

# Zeitstempel zum Programmstart
lasttime_lamps_on   = 0           
lasttime_lamps_off  = 0          
lasttime_airpump_on = 0            
lasttime_airpump_off= 0             

# Definition von Steuerparametern
lamps_on_time       = 60*60*24*7    # 24/7 an
lamps_off_time      = 0             # 0 Stunden
airpump_on_time     = 60*15         # 15 Minuten
airpump_off_time    = 60*15         # 15 Miuten
messzeit = 60*60*24*14 # Gesamtversuchszeit/s

# Initialisieren der Klassenobjekte
Lampen = WIRELESSSOCKET_control(pin=17, on_time=lamps_on_time, off_time=lamps_off_time)
Luftpumpe = WIRELESSSOCKET_control(pin=18, on_time=airpump_on_time, off_time=airpump_off_time)

# Starten des Timers für die Ausführungen
timer = time()

# Hauptschleife
while timer <= messzeit:

    if (Lampen.status == False) and (timer-lasttime_lamps_off >= lamps_off_time):
        Lampen.EIN()
        lasttime_lamps_on = timer

    if (Lampen.status == True) and (timer-lasttime_lamps_on >= lamps_on_time):
        Lampen.AUS()
        lasttime_lamps_off = timer

    if (Luftpumpe.status == False) and (timer-lasttime_airpump_off >= airpump_off_time):
        Luftpumpe.EIN()
        lasttime_airpump_on = timer

    if (Luftpumpe.status == True) and (timer-lasttime_airpump_on >= airpump_on_time):
        Lampen.AUS()
        lasttime_airpump_off = timer
