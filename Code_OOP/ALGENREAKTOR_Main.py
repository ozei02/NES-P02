# Skript zum Ausführen des Photobioreaktors

from PARAMETERS_Definition import parameters
from WIRELESSSOCKET_Classdefinition import WIRELESSSOCKET_control
from MOSFET_Classdefinition import MOSFET_control
from CAM_Classdefinition import CAM_control
from PHOTOSENSOR_Classdefinition import PHOTOSENSOR_reading
from PHPROBE_Classdefinition import PHPROBE_reading
from TEMPSENSOR_Classdefinition import TEMPSENSOR_reading
from time import time
from MEASUREMENT_Functions import measurement_bright, measurement_dark
import datetime

try:

    # Initialisieren der Zeitstempel der Objekte und Messungen
    lasttime_foto       = 0             # Zeitstempel Kameramodul
    lasttime_measurement= 0             # Zeitstempel Messungen
    lasttime_lamps_on   = 0             # Zeitstempel Lampen 
    lasttime_lamps_off  = 0             # Zeitstempel Lampen
    lasttime_airpump_on = 0             # Zeitstempel Pumpe
    lasttime_airpump_off= 0             # Zeitstempel Pumpe
    lasttime_fertilizer = 0             # Zeitstempel Düngepumpe
    datapoint = 0                       # Anzahl Messungen

    # Initialisieren der Aktoren
    lamps = WIRELESSSOCKET_control(pin=parameters.lamps_pin)
    airpump = WIRELESSSOCKET_control(pin=parameters.airpump_pin)
    co2gas = WIRELESSSOCKET_control(pin=parameters.co2gas_pin)
    fertilizerpump = MOSFET_control(pin=parameters.fertilizerpump_pin, dutycycle=parameters.fertilizerpump_dutycycle, startuptime=parameters.fertilizerpump_startuptime, actiontime=parameters.fertilizerpump_actiontime)

    # Initialisieren der Sensoren
    photosensor = PHOTOSENSOR_reading() # Photosensor
    ph_probe = PHPROBE_reading() # pH-Sonde
    T_sensor = TEMPSENSOR_reading() # Temperatursensor

    # Initialisieren der Kamera zur Fotoaufnahme
    cam = CAM_control()

    # Initialisieren der Timer
    startsec = time()                   # Zeitstartwert für die Messungen in s
    timer = time()	                    # Zeitvariable für Messtiming

    # Startprozedur der Düngepumpe
    fertilizerpump.startup()
    # if-Schleife welche betreten wird sobald die Durchflutung der Pumpe vom Nutzer bestätig wird
    if fertilizerpump.flooded == True:

        # Ausgabe der Startzeit des Programms
        now = datetime.datetime.now() # get current date and time
        date_time = now.strftime("%Y-%m-%d, %H:%M:%S") # timestamp of measurement
        print(f"{date_time}: Programmstart")

        # Start der Hauptschleife des Programms
        while timer-startsec <= parameters.runtime:

            # Durchführen der Messungen
            if timer-lasttime_measurement >= parameters.sampletime_measurements:
                lasttime_measurement = timer
                measurement_bright(lamps=lamps, airpump=airpump, photosensor=photosensor, ph_probe=ph_probe, T_sensor=T_sensor)
                measurement_dark(lamps=lamps, airpump=airpump, photosensor=photosensor, ph_probe=ph_probe, T_sensor=T_sensor)
                print(f"Messung {datapoint}/{parameters.datapoints_overall} abgeschlossen ...\n")
                datapoint += 1 

            # Steuern der Düngepumpe   
            if timer-lasttime_fertilizer >= parameters.fertilizerpump_off_time:
                lasttime_fertilizer = timer
                fertilizerpump.on()
                # Codeblock zur Ausgabe der Änderung zum eingeschalteten Zustand im Command Fenster
                now = datetime.datetime.now() # aktuelles Datum und Zeit
                date_time = now.strftime("%Y-%m-%d, %H:%M:%S") # Zeitstempel zu dem das Objekt geschaltet wird
                print(f"{date_time}: Düngung durchgeführt")

            # Luftpumpe ein-/ausschalten (Zeitsteuerung)
            if (airpump.status == False) and (timer-lasttime_airpump_off >= parameters.airpump_off_time):
                lasttime_airpump_on = timer
                airpump.on()
                # Codeblock zur Ausgabe der Änderung zum eingeschalteten Zustand im Command Fenster
                now = datetime.datetime.now() # aktuelles Datum und Zeit
                date_time = now.strftime("%Y-%m-%d, %H:%M:%S") # Zeitstempel zu dem das Objekt geschaltet wird
                print(f"{date_time}: Luftpumpe zeitgesteuert eingeschaltet nach {(parameters.airpump_off_time)/60:5.1f} Minuten")

            if (airpump.status == True) and (timer-lasttime_airpump_on >= parameters.airpump_on_time):
                lasttime_airpump_off = timer
                airpump.off()
                # Codeblock zur Ausgabe der Änderung zum eingeschalteten Zustand im Command Fenster
                now = datetime.datetime.now() # aktuelles Datum und Zeit
                date_time = now.strftime("%Y-%m-%d, %H:%M:%S") # Zeitstempel zu dem das Objekt geschaltet wird
                print(f"{date_time}: Luftpumpe zeitgesteuert ausgeschaltet nach {(parameters.airpump_on_time)/60:5.1f} Minuten")

            # Lampen ein-/ausschalten (Zeitsteuerung)
            if (lamps.status == False) and (timer-lasttime_lamps_off >= parameters.lamps_off_time):
                lasttime_lamps_on = timer
                lamps.on()
                # Codeblock zur Ausgabe der Änderung zum eingeschalteten Zustand im Command Fenster
                now = datetime.datetime.now() # aktuelles Datum und Zeit
                date_time = now.strftime("%Y-%m-%d, %H:%M:%S") # Zeitstempel zu dem das Objekt geschaltet wird
                print(f"{date_time}: Lampen zeitgesteuert eingeschaltet nach {(parameters.lamps_off_time)/60:5.1f} Minuten")

            if (lamps.status == True) and (timer-lasttime_lamps_on >= parameters.lamps_on_time):
                lasttime_lamps_off = timer
                lamps.off()  
                # Codeblock zur Ausgabe der Änderung zum eingeschalteten Zustand im Command Fenster
                now = datetime.datetime.now() # aktuelles Datum und Zeit
                date_time = now.strftime("%Y-%m-%d, %H:%M:%S") # Zeitstempel zu dem das Objekt geschaltet wird
                print(f"{date_time}: Lampen zeitgesteuert ausgeschaltet nach {(parameters.lamps_on_time)/60:5.1f} Minuten")

            # Aufnehmen der Fotos
            if timer-lasttime_foto >= parameters.sampletime_cam:
                lasttime_foto = timer
                # nur Fotos aufnehmen, wenn die Lampen an sind
                if lamps.status == True: 
                    cam.get_photo()

            # Steuerung der CO2-Begasung in Abhängigkeit vom pH-Wert

            # Mittelung des aktuellen pH-Werts aus Einzelmessungen
            pH_sum = 0
            for pH in range(parameters.datapoints_per_measuringpoint):
                pH_datapoint = ph_probe.measure()
                pH_sum = pH_sum + pH_datapoint
            pH_current = pH_sum/parameters.datapoints_per_measuringpoint

            # Ein- und Ausschalten der Funksteckdose je nach gemessenem pH-Wert
            if (co2gas.status == False) and (lamps.status == True) and (pH_current >= parameters.ph_max):
                co2gas.on()
                # Codeblock zur Ausgabe der Änderung zum eingeschalteten Zustand im Command Fenster
                now = datetime.datetime.now() # aktuelles Datum und Zeit
                date_time = now.strftime("%Y-%m-%d, %H:%M:%S") # Zeitstempel zu dem das Objekt geschaltet wird
                print(f"{date_time}: CO2-Begasung pH-Wert gesteuert gestartet (pH-Wert = {pH_current})")

            if (co2gas.status == True) and (pH_current <= parameters.ph_min):
                co2gas.off()
                # Codeblock zur Ausgabe der Änderung zum eingeschalteten Zustand im Command Fenster
                now = datetime.datetime.now() # aktuelles Datum und Zeit
                date_time = now.strftime("%Y-%m-%d, %H:%M:%S") # Zeitstempel zu dem das Objekt geschaltet wird
                print(f"{date_time}: CO2-Begasung pH-Wert gesteuert beendet (pH-Wert = {pH_current})")

            # Setzen des Timers für den nächsten Durchlauf
            timer = time()

except KeyboardInterrupt:
    # Ausschalten der Düngepumpe
    fertilizerpump.off()
    # Ausschalten aller Objekte die per Funksteckdose gesteuert werden
    lamps.off()
    airpump.off()
    co2gas.off()
    # Ausschalten der LED vom Photosensor
    photosensor.led = False
    # Bereinigen der Belegung der GPIO Pins (Gilt nicht nur für die Düngerpumpe sondern für alle Objekte)
    fertilizerpump.cleanup()
    print("\nSensor-LED aus - Lüftung aus - Lampen aus - Düngerpumpe aus - CO2-Diffusoren aus - PROGRAMMENDE")