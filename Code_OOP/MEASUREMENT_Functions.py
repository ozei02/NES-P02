import csv
import datetime
from WIRELESSSOCKET_Test2 import airpump, lamps
import time
from PHOTOSENSOR_Classdefinition import PHOTOSENSOR_reading
from PHPROBE_Classdefinition import PHPROBE_reading
from TEMPSENSOR_Classdefinition import TEMPSENSOR_reading
from PARAMETERS_Definition import parameters

# Erstellen der Objekte für die einzelnen Sensoren
photosensor = PHOTOSENSOR_reading() # Photosensor
ph_probe = PHPROBE_reading() # pH-Sonde
T_sensor = TEMPSENSOR_reading() # Temperatursensor

# Funktion zum Abspeichern der Messwerte in einer csv-Datei
def SAVEDATA(photosensor_values, phprobe_values, temp_values, filename):
    values = [
            photosensor_values.sensor.channel_415nm, photosensor_values.sensor.channel_445nm, photosensor_values.sensor.channel_480nm,
            photosensor_values.sensor.channel_515nm, photosensor_values.sensor.channel_555nm, photosensor_values.sensor.channel_590nm,
            photosensor_values.sensor.channel_630nm, photosensor_values.sensor.channel_680nm, photosensor_values.sensor.channel_clear,
            photosensor_values.sensor.channel_nir, phprobe_values, temp_values, photosensor_values.sensor.algae_concentration
            ]
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        # Füge den Zeitstempel zu den Sensorwerten hinzu
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_row = [timestamp] + values
        writer.writerow(data_row)
        print(f"Daten gespeichert: {data_row}")

# Messung mit Lampen an und Pumpe aus
def measurement_bright():

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
        lamps.on_for_measurement()
    if airpump.status == True:
        airpump.off_for_measurement()
    time.sleep(2) # Beruhigungszeit für die Messung

    # Schleife über die Anzahl der Messungen pro Messpunkt
    for datapoint_bright in range(parameters.datapoints_per_measuringpoint):

        # Aufnehmen des Messzeitpunkts
        now = datetime.datetime.now()
        date_time_bright = now.strftime("%Y-%m-%d, %H:%M:%S") 

        # Aufnehmen der Messwerte
        photosensor.read_channels()
        photosensor.get_algae_concentration()
        ph_probe.measure()
        T_sensor.tempC(0)

        # Abspeichern der Messwerte
        SAVEDATA(photosensor_values=photosensor, phprobe_values=ph_probe, temp_values=T_sensor, filename=parameters.filename_bright)

        # Ausgabe pro Messpunkt
        print(f"{date_time_bright}: Einzelmessung mit Lampen an {datapoint_bright}/{parameters.datapoints_per_measuringpoint-1} done")

    # Zurückschalten der Schaltobjekte auf den Ausgangszustand
    if lamps.statusbeforemeasurement == True:
        lamps.on_for_measurement()
    if lamps.statusbeforemeasurement == False:
        lamps.off_for_measurement()
    if airpump.statusbeforemeasurement == True:
        airpump.on_for_measurement()
    if airpump.statusbeforemeasurement == False:
        airpump.off_for_measurement() 

# Messung mit Lampen aus und Pumpen aus
def measurement_dark():

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
        lamps.off_for_measurement()
    if airpump.status == True:
        airpump.off_for_measurement()
    time.sleep(2) # Beruhigungszeit für die Messung

    # Schleife über die Anzahl der Messungen pro Messpunkt
    for datapoint_dark in range(parameters.datapoints_per_measuringpoint):

        # Aufnehmen des Messzeitpunkts
        now = datetime.datetime.now()
        date_time_dark = now.strftime("%Y-%m-%d, %H:%M:%S") 

        # Aufnehmen der Messwerte
        photosensor.read_channels()
        photosensor.get_algae_concentration()
        ph_probe.measure()
        T_sensor.tempC(0)

        # Abspeichern der Messwerte
        SAVEDATA(photosensor_values=photosensor, phprobe_values=ph_probe, temp_values=T_sensor, filename=parameters.filename_dark)

        # Ausgabe pro Messpunkt
        print(f"{date_time_dark}: Einzelmessung mit Lampen aus {datapoint_dark}/{parameters.datapoints_per_measuringpoint-1} done")

    # Ausschalten der LED des Photosensors
    photosensor.led = False

    # Zurückschalten der Schaltobjekte auf den Ausgangszustand
    if lamps.statusbeforemeasurement == True:
        lamps.on_for_measurement()
    if lamps.statusbeforemeasurement == False:
        lamps.off_for_measurement()
    if airpump.statusbeforemeasurement == True:
        airpump.on_for_measurement()
    if airpump.statusbeforemeasurement == False:
        airpump.off_for_measurement()  