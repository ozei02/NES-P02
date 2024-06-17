import csv
import datetime
import time
from PARAMETERS_Definition import parameters

# Funktion zum Abspeichern der Messwerte in einer csv-Datei
def SAVEDATA(photosensor_values, phprobe_values, temp_values, filename):
    values = [
            photosensor_values.sensor.channel_415nm, photosensor_values.sensor.channel_445nm, photosensor_values.sensor.channel_480nm,
            photosensor_values.sensor.channel_515nm, photosensor_values.sensor.channel_555nm, photosensor_values.sensor.channel_590nm,
            photosensor_values.sensor.channel_630nm, photosensor_values.sensor.channel_680nm, photosensor_values.sensor.channel_clear,
            photosensor_values.sensor.channel_nir, phprobe_values, temp_values, photosensor_values.algae_concentration
            ]
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        # Füge den Zeitstempel zu den Sensorwerten hinzu
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_row = [timestamp] + values
        writer.writerow(data_row)
        print(f"Daten gespeichert: {data_row}")

# Messung mit Lampen an und Pumpe aus
def measurement_bright(lamps, airpump, photosensor, ph_probe, T_sensor):

    # Ausgabe zum Start der Messung
    print("Messung mit Hintergrundbeleuchtung gestartet")

    # Status der Schaltobjekte vor der Messung erfassen
    if lamps.status == True:
        lamps.statusbeforemeasurement = True
    else:
        lamps.statusbeforemeasurement = False
    if airpump.status == True:
        airpump.statusbeforemeasurement = True
    else:
        airpump.statusbeforemeasurement = False

    # Status von Lampen und Pumpe anpassen
    if lamps.status == False:
        lamps.on()
        # Codeblock zur Ausgabe der Änderung zum eingeschalteten Zustand im Command Fenster
        now = datetime.datetime.now() # aktuelles Datum und Zeit
        date_time = now.strftime("%Y-%m-%d, %H:%M:%S") # Zeitstempel zu dem das Objekt geschaltet wird
        print(f"{date_time}: Lampen für Messung eingeschaltet")

    if airpump.status == True:
        airpump.off()
        # Codeblock zur Ausgabe der Änderung zum eingeschalteten Zustand im Command Fenster
        now = datetime.datetime.now() # aktuelles Datum und Zeit
        date_time = now.strftime("%Y-%m-%d, %H:%M:%S") # Zeitstempel zu dem das Objekt geschaltet wird
        print(f"{date_time}: Luftpumpe für Messung ausgeschaltet")

    time.sleep(2) # Beruhigungszeit für die Messung

    # Schleife über die Anzahl der Messungen pro Messpunkt
    for datapoint_bright in range(parameters.datapoints_per_measuringpoint):

        # Aufnehmen des Messzeitpunkts
        now = datetime.datetime.now()
        date_time_bright = now.strftime("%Y-%m-%d, %H:%M:%S") 

        # Aufnehmen der Messwerte
        photosensor.read_channels()
        photosensor.get_algae_concentration()
        ph_value = ph_probe.measure()
        T_value = T_sensor.tempC(0)

        # Abspeichern der Messwerte
        SAVEDATA(photosensor_values=photosensor, phprobe_values=ph_value, temp_values=T_value, filename=parameters.filename_bright)

        # Ausgabe pro Messpunkt
        print(f"{date_time_bright}: Einzelmessung mit Lampen an {datapoint_bright}/{parameters.datapoints_per_measuringpoint-1} done")

    # Zurückschalten der Schaltobjekte auf den Ausgangszustand
    if lamps.statusbeforemeasurement == True:
        lamps.on()
    if lamps.statusbeforemeasurement == False:
        lamps.off()
    if airpump.statusbeforemeasurement == True:
        airpump.on()
    if airpump.statusbeforemeasurement == False:
        airpump.off() 

    # Codeblock zur Ausgabe der Änderung zum eingeschalteten Zustand im Command Fenster
    now = datetime.datetime.now() # aktuelles Datum und Zeit
    date_time = now.strftime("%Y-%m-%d, %H:%M:%S") # Zeitstempel zu dem das Objekt geschaltet wird
    print(f"{date_time}: Zustand vor Messung wieder hergestellt") 

# Messung mit Lampen aus und Pumpen aus
def measurement_dark(lamps, airpump, photosensor, ph_probe, T_sensor):

    # Ausgabe zum Start der Messung
    print("Messung ohne Hintergrundbeleuchtung gestartet")

    # LED des Photosensors einschalten
    photosensor.led = True

    # Status der Schaltobjekte vor der Messung erfassen
    if lamps.status == True:
        lamps.statusbeforemeasurement = True
    else:
        lamps.statusbeforemeasurement = False
    if airpump.status == True:
        airpump.statusbeforemeasurement = True
    else:
        airpump.statusbeforemeasurement = False

    # Status von Lampen und Pumpe anpassen
    if lamps.status == True:
        lamps.off()
        # Codeblock zur Ausgabe der Änderung zum eingeschalteten Zustand im Command Fenster
        now = datetime.datetime.now() # aktuelles Datum und Zeit
        date_time = now.strftime("%Y-%m-%d, %H:%M:%S") # Zeitstempel zu dem das Objekt geschaltet wird
        print(f"{date_time}: Lampen für Messung ausgeschaltet")

    if airpump.status == True:
        airpump.off()
        # Codeblock zur Ausgabe der Änderung zum eingeschalteten Zustand im Command Fenster
        now = datetime.datetime.now() # aktuelles Datum und Zeit
        date_time = now.strftime("%Y-%m-%d, %H:%M:%S") # Zeitstempel zu dem das Objekt geschaltet wird
        print(f"{date_time}: Luftpumpe für Messung ausgeschaltet")

    time.sleep(2) # Beruhigungszeit für die Messung

    # Schleife über die Anzahl der Messungen pro Messpunkt
    for datapoint_dark in range(parameters.datapoints_per_measuringpoint):

        # Aufnehmen des Messzeitpunkts
        now = datetime.datetime.now()
        date_time_dark = now.strftime("%Y-%m-%d, %H:%M:%S") 

        # Aufnehmen der Messwerte
        photosensor.read_channels()
        photosensor.get_algae_concentration()
        ph_value = ph_probe.measure()
        T_value = T_sensor.tempC(0)

        # Abspeichern der Messwerte
        SAVEDATA(photosensor_values=photosensor, phprobe_values=ph_value, temp_values=T_value, filename=parameters.filename_dark)

        # Ausgabe pro Messpunkt
        print(f"{date_time_dark}: Einzelmessung mit Lampen aus {datapoint_dark}/{parameters.datapoints_per_measuringpoint-1} done")

    # Ausschalten der LED des Photosensors
    photosensor.led = False

    # Zurückschalten der Schaltobjekte auf den Ausgangszustand
    if lamps.statusbeforemeasurement == True:
        lamps.on()
    if lamps.statusbeforemeasurement == False:
        lamps.off()
    if airpump.statusbeforemeasurement == True:
        airpump.on()
    if airpump.statusbeforemeasurement == False:
        airpump.off()

    # Codeblock zur Ausgabe der Änderung zum eingeschalteten Zustand im Command Fenster
    now = datetime.datetime.now() # aktuelles Datum und Zeit
    date_time = now.strftime("%Y-%m-%d, %H:%M:%S") # Zeitstempel zu dem das Objekt geschaltet wird
    print(f"{date_time}: Zustand vor Messung wieder hergestellt")  