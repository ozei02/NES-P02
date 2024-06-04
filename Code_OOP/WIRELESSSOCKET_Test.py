from WIRELESSSOCKET_Classdefinition import WIRELESSSOCKET_control     

# Testparameter
lamps_on_time = 15
lamps_off_time = 15
airpump_on_time = 30
airpump_off_time = 30

# Initialisieren der Klassenobjekte
Lampen = WIRELESSSOCKET_control(pin=17, on_time=lamps_on_time, off_time=lamps_off_time)
Luftpumpe = WIRELESSSOCKET_control(pin=18, on_time=airpump_on_time, off_time=airpump_off_time)

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
