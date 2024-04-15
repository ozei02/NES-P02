# Gesamtsteuerung Algenreaktor kion war hier das dritte mal heute   Finn auch
# Finns Branch Test
''' Änderungen für nächste Version: 
- High-Signal über freien PIN als Fototrigger für den Foto-Raspi, dort Pause nach Foto einbauen, damit
  hier genug Zeit beibt, den Trigger wieder wegzunehmen
- Temperaturmessung hier einbinden
'''
# Version 004: Temperatursensorintegration
# Version 003: Zeitstempel bei print-Ausgaben zur Kontrolle, Bugfix Verzögerungszeit bei Lampen-an-Messung, Bugfix Lampen/Pumpensteuerung
# Version 002: Integration pH-Sensor über AD-Karte
# Funksteckdose --> Lampen
# Funksteckdosen --> Lüftung
# Photosensor Adafruit AS7341 über IC2
# pH-Messung
# (Temperaturmessung)
# (Fotos)

from time import sleep, time
import board
import busio
from adafruit_as7341 import AS7341
import matplotlib.pyplot as plt
import numpy as np
import datetime
import csv
import os
import glob
from gpiozero import LED # Standard-Device, wird für Steckdosenrelais benutzt
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from sklearn.linear_model import LinearRegression

i2c = board.I2C()  # verwendet board.SCL und board.SDA
sensor = AS7341(i2c)

i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)

# Klassendefinition für Temperatursensoren DS18B20 ######################
class DS18B20:
    
    def __init__(self):
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '28*')
        self._count_devices = len(device_folder)
        self._devices = list()
        i = 0
        while i < self._count_devices:
            self._devices.append(device_folder[i] + '/w1_slave')
            i += 1
            
    def device_names(self):
        names = list()
        for i in range(self._count_devices):
            names.append(self._devices[i])
            temp = names[i][20:35]
            names[i] = temp
        
        return names
    
# (one tab)
    def _read_temp(self, index):
        f = open(self._devices[index], 'r')
        lines = f.readlines()
        f.close()
        return lines
    
    def tempC(self, index = 0):
        lines = self._read_temp(index)
        retries = 5
        while (lines[0].strip()[-3:] != 'YES') and (retries > 0):
            time.sleep(0.01)
            lines = self._read_temp(index)
            retries -= 1

        if retries == 0:
            return 998

        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp = lines[1][equals_pos + 2:]
            return float(temp) / 1000
        else:
            return 999 # error
        
    def device_count(self):
        return self._count_devices
#######################################################################

devices = DS18B20()
count = devices.device_count()
names = devices.device_names()

# Globale Variablen
filename1           = "Messreihe4_dark_JP004.csv"
filename2           = "Messreihe4_bright_JP004.csv"
lamps               = False         # Status für Steckdose A, Lampen
airpump             = False         # Status für Steckdose B, Luftpumpe
algae_concentration = 0
mmax                = 5             # Wiederholungsmessungen für einen Messpunkt

lamps_on_time       = 60*60*24*7    # 24/7 an
lamps_off_time      = 0             # 0 Stunden
airpump_on_time     = 60*15         # 15 Minuten
airpump_off_time    = 60*15         # 15 Miuten
abtastzeit_AS7341   = 60*30	        # Abtastrate für Messungen einstellen
messzeit            = 60*60*24*14   # Gesamtmesszeit, bis das Programm automatisch beendet wird

verhaeltnis_reaktor_zu_probe = 0.35635681 # Verhältnis der Reflexionswerte zwischen Reaktor und Probe
anzahl_AS7341 = messzeit/abtastzeit_AS7341# Anzahl der Messpunkte

# Kalibrierwerte der pH-Sonde mit Referenzlösungen gemessen
x = np.array([2.016, 1.515, 1.119]).reshape((-1, 1))	# gemessene Spannungswerte für Kalibrierlösungen
y = np.array([4.0, 6.88, 9.23]) # pH-Werte der Kalibrierlösungen
pHmodel = LinearRegression().fit(x, y) # lineares Kalibriermodell pH-Sonde


######## STECKDOSENMODUL ###########################################################
# Pins zuordnen und Steckdosen als ausgeschaltet initialisieren
steckdose_A = LED(17)	# BCM-Nummer 17 = Pin 11 als Impulssignal für Relais A
steckdose_B = LED(18)	# BCM-Nummer 18 = Pin 12 als Impulssignal für Relais A
steckdose_on = LED(27)  # BCM-Nummer 27 = Pin 13 als Impulssignal für Relais on
steckdose_off = LED(22) # BCM-Nummer 22 = Pin 15 als Impulssignal für Relais off
tastenzeit = 0.2        # so lange wir ein Relais angesteuert

# alle Relais ausschalten (ACHTUNG positiver Impuls schaltet die Relais aus)
# ACHTUNG "on" bedeutet hier "off"
steckdose_A.on()
steckdose_B.on()
steckdose_on.on()
steckdose_off.on()

def wireless_socket(socket, status):	# socket: ("A","B") status: ("on", "off")
	if socket == "A" and status =="on":
		steckdose_A.off()		# Auswahl der zu schaltenden Steckdose
		steckdose_on.off()		# Auswahl des Schaltzusztandes
		#print(f"Socket {socket} --> {status}")
		sleep(tastenzeit)	    # Wartezeit für zuverlässige Schaltzeit
		steckdose_A.on()		# Schalter neutralisieren
		steckdose_on.on()		# Schalter neutralisieren
		lamps = True            # Statusvariable Hauptprogramm setzen
		
	if socket == "A" and status =="off":
		steckdose_A.off()		# Auswahl der zu schaltenden Steckdose
		steckdose_off.off()		# Auswahl des Schaltzusztandes
		#print(f"Socket {socket} --> {status}")
		sleep(tastenzeit)	    # Wartezeit für zuverlässige Schaltzeit
		steckdose_A.on()		# Schalter neutralisieren
		steckdose_off.on()		# Schalter neutralisieren
		lamps = False           # Statusvariable Hauptprogramm setzen
		
	if socket == "B" and status =="on":
		steckdose_B.off()		# Auswahl der zu schaltenden Steckdose
		steckdose_on.off()		# Auswahl des Schaltzusztandes
		#print(f"Socket {socket} --> {status}")
		sleep(tastenzeit)	    # Wartezeit für zuverlässige Schaltzeit
		steckdose_B.on()		# Schalter neutralisieren
		steckdose_on.on()		# Schalter neutralisieren
		airpump = True          # Statusvariable Hauptprogramm setzen
		
	if socket == "B" and status =="off":
		steckdose_B.off()		# Auswahl der zu schaltenden Steckdose
		steckdose_off.off()		# Auswahl des Schaltzusztandes
		#print(f"Socket {socket} --> {status}")
		sleep(tastenzeit)	    # Wartezeit für zuverlässige Schaltzeit
		steckdose_B.on()		# Schalter neutralisieren
		steckdose_off.on()		# Schalter neutralisieren
		airpump = False  	    # Statusvariable Hauptprogramm setzen
####################################################################################

###### MODUL PHOTOSENSOR #############################################################
# Messmodus Initialisierung: Definiert den Startmessmodus als "Reactor"
messmodus = "Reactor"

# Aktiviert die LED und setzt den LED-Strom
sensor.led_current = 5  # Setzt den LED-Strom auf 5mA
#sensor.led = True  # Schaltet die LED an
#print("Sensor-LED ein")

channels = ['415nm', '445nm', '480nm', '515nm', '555nm', '590nm', '630nm', '680nm', 'Clear', 'NIR']
colors = ['violet', 'indigo', 'blue', 'cyan', 'green', 'yellow', 'orange', 'red', 'grey', 'black']

def get_sensor_value_at_clear(adjust_for_mode=True):
    # Liest den Sensorwert bei clear. Passt den Wert an, wenn im "Reaktor"-Modus
    #sensor.led = True	# LED einschalten
    #sleep(1)
    raw_value = sensor.channel_clear
    #sensor.led = False	# LED ausschalten
    #print(f"Rohwert vor Anpassung: {raw_value}")  # Debugging-Ausgabe
    if adjust_for_mode:
        if messmodus == "Reaktor":
            adjusted_value = raw_value / verhaeltnis_reaktor_zu_probe
            print(f"Angepasster Wert (Reaktor): {adjusted_value}")  # Debugging-Ausgabe
            return adjusted_value
        elif messmodus == "Probenbox":
            # Optional: Hier könnte eine Anpassung für die Probenbox erfolgen
            print(f"Angepasster Wert (Probenbox): {raw_value}")  # Debugging-Ausgabe
            return raw_value
    return raw_value

def calculate_algae_concentration(sensor_value):
    global algae_concentration
    # Berechnet die Algenkonzentration basierend auf dem Sensorwert
    m = -1.0500363424809021e-06
    b = 39040.888573888915
    algae_concentration = (sensor_value - b) / m

def save_to_csv(sensor_values, algae_concentration, filename):
    """
    Speichert Sensorwerte, Algenkonzentration und Zeitstempel in einer CSV-Datei.
    :param sensor_values: Liste von Sensorwerten.
    :param algae_concentration: Berechnete Algenkonzentration.
    """
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        # Füge den Zeitstempel zu den Sensorwerten hinzu
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_row = [timestamp] + sensor_values + [algae_concentration]
        writer.writerow(data_row)
        print(f"Daten gespeichert: {data_row}")
######################################################################################

try:
    # Initialisierung
    lampenstatus_vor_messung = False    # Indikator, um die Lampen nach der Messung wieder in den Ursprungszustand zu versetzen
    airpumpstatus_vor_messung = False
    lasttime_photosensor= 0             # Zeitstempel Photosensormessung
    lasttime_lamps_on   = 0             # Zeitstempel Lampen 
    lasttime_lamps_off  = 0             # Zeitstempel Lampen
    lasttime_airpump_on = 0             # Zeitstempel Pumpe
    lasttime_airpump_off= 0             # Zeitstempel Pumpe
    messpunkt           = 0    
    startsec = time()                   # Zeitstartwert für die Messungen in s
    timer = time()	                    # Zeitvariable für Messtiming
    #wireless_socket("A", "on")         # Lampen einschalten
    
    now = datetime.datetime.now() # get current date and time
    date_time = now.strftime("%Y-%m-%d, %H:%M:%S") # timestamp of measurement
    print(f"{date_time}: Programmstart")
    
    # Hauptschleife zur Steuerung und Messung
    while timer-startsec <= messzeit:
                   
        # Pumpe ein-/ausschalten (Zeitsteuerung)###################################
        if (airpump == False) and (timer-lasttime_airpump_off >= airpump_off_time):
            lasttime_airpump_on = timer
            wireless_socket("B", "on") # Lüftung einschalten
            airpump = True
            now = datetime.datetime.now() # get current date and time
            date_time = now.strftime("%Y-%m-%d, %H:%M:%S") # timestamp of measurement
            print(f"{date_time}: Luftpumpe zeitgesteuert eingeschaltet nach {(timer-lasttime_airpump_off)/60:5.1f} Minuten")
                
        if (airpump == True) and (timer-lasttime_airpump_on >= airpump_on_time):
            lasttime_airpump_off = timer
            wireless_socket("B", "off") # Lüftung ausschalten
            airpump = False
            now = datetime.datetime.now() # get current date and time
            date_time = now.strftime("%Y-%m-%d, %H:%M:%S") # timestamp of measurement
            print(f"{date_time}: Luftpumpe zeitgesteuert ausgeschaltet nach {(timer-lasttime_airpump_on)/60:5.1f} Minuten")
            
        # Lampen ein-ausschalten (Zeitsteuerung) ################################
        if (lamps == False) and (timer-lasttime_lamps_off >= lamps_off_time):
            lasttime_lamps_on = timer
            wireless_socket("A", "on") # Lampen einschalten
            lamps = True
            now = datetime.datetime.now() # get current date and time
            date_time = now.strftime("%Y-%m-%d, %H:%M:%S") # timestamp of measurement
            print(f"{date_time}: Lampen zeitgesteuert eingeschaltet nach {(timer-lasttime_lamps_off)/60:5.1f} Minuten")
                
        if (lamps == True) and (timer-lasttime_lamps_on >= lamps_on_time):
            lasttime_lamps_off = timer
            wireless_socket("A", "off") # Lampen ausschalten
            lamps = False
            now = datetime.datetime.now() # get current date and time
            date_time = now.strftime("%Y-%m-%d, %H:%M:%S") # timestamp of measurement
            print(f"{date_time}: Lampen zeitgesteuert ausgeschaltet nach {(timer-lasttime_lamps_on)/60:5.1f} Minuten")
        
        # Photosensormessung AS7341 #############################################
        if timer-lasttime_photosensor >= abtastzeit_AS7341:     
            
            lasttime_photosensor = timer
            
            sensor.led = True	# LED einschalten
            now = datetime.datetime.now() # get current date and time
            date_time = now.strftime("%Y-%m-%d, %H:%M:%S") # timestamp of measurement
            print(f"{date_time}: Sensor-LED ein")
                        
            # Messung mit Lampen aus und Pumpe aus
            if lamps == True:
                lampenstatus_vor_messung = True
                now = datetime.datetime.now() # get current date and time
                date_time = now.strftime("%Y-%m-%d, %H:%M:%S") # timestamp of measurement
                print(f"{date_time}: Lampen für Messung ausgeschaltet")
                wireless_socket("A", "off") # Lampen ausschalten
                lamps = False
            else:
                lampenstatus_vor_messung = False    
                
            if airpump == True:
                wireless_socket("B", "off") # Lüftung ausschalten
                print(f"{date_time}: Luftpumpe für Messung ausgeschaltet")
                airpumpstatus_vor_messung = True
                airpump = False
            else:  
                airpumpstatus_vor_messung = False    
                
            sleep(2) # Beruhigungszeit
            
            for messung in range(mmax): # mmax Messungen durchführen
                now = datetime.datetime.now() # get current date and time
                date_time = now.strftime("%Y-%m-%d, %H:%M:%S") # timestamp of measurement
                
                # pH-Messung als Spannungswert und Umrechnung in pH
                chan = AnalogIn(ads, ADS.P0)
                spannung = chan.voltage
                pH = chan.voltage * pHmodel.coef_[0] + pHmodel.intercept_
                ############
                
                # Temperaturmessungen (theoretisch für mehrere Sensoren möglich)
                temperature = devices.tempC(0)
                #####################
                
                values = [
                        sensor.channel_415nm, sensor.channel_445nm, sensor.channel_480nm,
                        sensor.channel_515nm, sensor.channel_555nm, sensor.channel_590nm,
                        sensor.channel_630nm, sensor.channel_680nm, sensor.channel_clear,
                        sensor.channel_nir, pH, temperature
                    ]
                print(f"{date_time}: Einzelmessung mit Diodenlicht {messung}/{mmax-1} done")
                
                sensor_value_clear = get_sensor_value_at_clear()
                
                calculate_algae_concentration(sensor_value_clear)
                save_to_csv(values, algae_concentration, filename1)
                
                #print(f"Messung {messung}: {values}")
                #if messung == 0:
                #    messreihe = [messung, values]
                #else:
                #    messreihe.append([messung, values])
            
            # Messung mit Lampen an und Pumpe aus
            wireless_socket("A", "on") # Lampen anschalten
            lamps = True
            now = datetime.datetime.now() # get current date and time
            date_time = now.strftime("%Y-%m-%d, %H:%M:%S") # timestamp of measurement
            print(f"{date_time}: Lampen für Messung eingeschaltet")
            sleep(1) # Verzögerung, damit Lampen sicher an sind
            
            for messung in range(mmax): # mmax Messungen durchführen
                now = datetime.datetime.now() # get current date and time
                date_time = now.strftime("%Y-%m-%d, %H:%M:%S") # timestamp of measurement
                
                # pH-Messung
                chan = AnalogIn(ads, ADS.P0)
                spannung = chan.voltage
                pH = chan.voltage * pHmodel.coef_[0] + pHmodel.intercept_
                ############
                
                # Temperaturmessungen
                temperature = devices.tempC(0)
                #####################
                
                values = [
                        sensor.channel_415nm, sensor.channel_445nm, sensor.channel_480nm,
                        sensor.channel_515nm, sensor.channel_555nm, sensor.channel_590nm,
                        sensor.channel_630nm, sensor.channel_680nm, sensor.channel_clear,
                        sensor.channel_nir, pH, temperature
                    ]
                print(f"{date_time}: Einzelmessung mit Lampen an {messung}/{mmax-1} done")
                
                sensor_value_clear = get_sensor_value_at_clear()
                
                calculate_algae_concentration(sensor_value_clear)
                save_to_csv(values, algae_concentration, filename2)
                
                #print(f"Messung {messung}: {values}")
                #if messung == 0:
                #    messreihe2 = [messung, values]
                #else:
                #    messreihe2.append([messung, values])
                        
            # print(f"\nMessreihe: {messreihe2}")
            # hier fehlt noch eine Mittelwertbildung über Messreihe als 2d numpy-array
            
            sensor.led = False  # Schaltet die LED aus
            
            if lampenstatus_vor_messung == False:
                wireless_socket("A", "off") # Lampen ausschalten
                lamps = False
                now = datetime.datetime.now() # get current date and time
                date_time = now.strftime("%Y-%m-%d, %H:%M:%S") # timestamp of measurement
                print(f"{date_time}: Lampen nach Messung ausgeschaltet")
                
            if airpumpstatus_vor_messung == True:
                wireless_socket("B", "on") # Pumpe anschalten
                airpump = True
                now = datetime.datetime.now() # get current date and time
                date_time = now.strftime("%Y-%m-%d, %H:%M:%S") # timestamp of measurement
                print(f"{date_time}: Luftpumpe nach Messung eingeschaltet")
                
            print(f"{date_time}: Sensor-LED aus")
            print(f"Messung {messpunkt}/{anzahl_AS7341} abgeschlossen ...\n")
            messpunkt += 1
            
        timer = time()
       
except KeyboardInterrupt:
    wireless_socket("A", "off") # Lampen ausschalten
    wireless_socket("B", "off") # Lüftung ausschalten
    sensor.led = False  # Schaltet die LED aus
    print("\nSensor-LED aus - Lüftung aus - Lampen aus - PROGRAMMENDE")
