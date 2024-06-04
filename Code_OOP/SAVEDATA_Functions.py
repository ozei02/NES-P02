import csv
import datetime

def SAVEDATA(photosensor_values, phprobe_values, temp_values, filename):
    values = [
            photosensor_values.channel_415nm, photosensor_values.channel_445nm, photosensor_values.channel_480nm,
            photosensor_values.channel_515nm, photosensor_values.channel_555nm, photosensor_values.channel_590nm,
            photosensor_values.channel_630nm, photosensor_values.channel_680nm, photosensor_values.channel_clear,
            photosensor_values.channel_nir, phprobe_values, temp_values, photosensor_values.algae_concentration
            ]
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        # Füge den Zeitstempel zu den Sensorwerten hinzu
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_row = [timestamp] + values
        writer.writerow(data_row)
        print(f"Daten gespeichert: {data_row}")