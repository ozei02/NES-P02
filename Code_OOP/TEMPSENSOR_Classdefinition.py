import glob # Ermöglicht das Durchsuchen von Dateisystemen nach Dateipfaden, die bestimmten Mustern entsprechen
import os # Ermöglicht Interaktion mit dem Betriebssystem auf dem Python ausgeführt wird
import time

# Klassendefinition für Temperatursensoren DS18B20
class TEMPSENSOR_reading:

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
            self.tempC_current = 998

        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp = lines[1][equals_pos + 2:]
            self.tempC_current = float(temp) / 1000
        else:
            self.tempC_current = 999 # error
        
    def device_count(self):
        return self._count_devices