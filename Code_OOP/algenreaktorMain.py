from PARAMETERS_Definition import parameters
from WIRELESSSOCKET_Classdefinition import WIRELESSSOCKET_control
from MOSFET_Classdefinition import MOSFET_control
from CAM_Classdefinition import CAM_control
from MEASUREMENT_Functions import photosensor
from time import time
from MEASUREMENT_Functions import measurement_bright, measurement_dark
import datetime

# Initialisieren der Zeitstempel der Objekte und Messungen
lasttime_foto       = 0             # Zeitstempel Kameramodul
lasttime_measurement= 0             # Zeitstempel Messungen
lasttime_lamps_on   = 0             # Zeitstempel Lampen 
lasttime_lamps_off  = 0             # Zeitstempel Lampen
lasttime_airpump_on = 0             # Zeitstempel Pumpe
lasttime_airpump_off= 0             # Zeitstempel Pumpe
lasttime_fertilizer = 0             # Zeitstempel Düngepumpe

# Initialisieren der Aktoren
lamps = WIRELESSSOCKET_control(pin=parameters.lamps_pin, on_time=parameters.lamps_on_time, off_time=parameters.lamps_off_time)
airpump = WIRELESSSOCKET_control(pin=parameters.airpump_pin, on_time=parameters.airpump_on_time, off_time=parameters.airpump_off_time)
fertilizerpump = MOSFET_control(pin=parameters.fertilizerpump_pin, dutycycle=parameters.fertilizerpump_dutycycle, startuptime=parameters.fertilizerpump_startuptime, actiontime=parameters.fertilizerpump_actiontime)

# Initialisieren der Kamera zur Fotoaufnahme
cam = CAM_control()

# Initialisieren der Timer
startsec = time()                   # Zeitstartwert für die Messungen in s
timer = time()	                    # Zeitvariable für Messtiming

try:
    # Startprozedur der Düngepumpe
    fertilizerpump.startup()
    if fertilizerpump.flooded == True:

        # Ausgabe der Startzeit des Programms
        now = datetime.datetime.now() # get current date and time
        date_time = now.strftime("%Y-%m-%d, %H:%M:%S") # timestamp of measurement
        print(f"{date_time}: Programmstart")

        # Start der Hauptschleife des Programms
        while timer-startsec <= parameters.runtime:

            # Pumpe ein-/ausschalten (Zeitsteuerung)
            if (airpump.status == False) and (timer-lasttime_airpump_off >= parameters.airpump_off_time):
                lasttime_airpump_on = timer
                airpump.on()

            if (airpump.status == True) and (timer-lasttime_airpump_on >= parameters.airpump_on_time):
                lasttime_airpump_off = timer
                airpump.off()

            # Licht ein-/ausschalten (Zeitsteuerung)
            if (lamps.status == False) and (timer-lasttime_lamps_off >= parameters.lamps_off_time):
                lasttime_lamps_on = timer
                lamps.on()

            if (lamps.status == True) and (timer-lasttime_lamps_on >= parameters.lamps_on_time):
                lasttime_lamps_off = timer
                lamps.off()  

            # Steuern der Düngepumpe   
            if timer-lasttime_fertilizer >= parameters.fertilizationpump_off_time:
                fertilizerpump.on()
                lasttime_fertilizer = timer

            # Durchführen der Messungen
            if timer-lasttime_measurement >= parameters.sampletime_measurements:
                lasttime_measurement = timer
                measurement_bright()
                measurement_dark() 

            # Aufnehmen der Fotos
            if timer-lasttime_foto >= parameters.sampletime_cam:
                lasttime_foto = timer
                # nur Fotos aufnehmen, wenn die Lampen an sind
                if lamps.status == True: 
                    cam.get_photo()

            timer = time()

except KeyboardInterrupt:
    # Ausschalten der Düngepumpe
    fertilizerpump.off()
    fertilizerpump.cleanup()
    # Ausschalten aller Objekte die per Funksteckdose gesteuert werden
    lamps.off()
    airpump.off()
    # Ausschalten der LED vom Photosensor
    photosensor.led = False
    print("\nSensor-LED aus - Lüftung aus - Lampen aus - Düngerpumpe aus - PROGRAMMENDE")