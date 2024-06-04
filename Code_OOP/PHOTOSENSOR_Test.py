from PHOTOSENSOR_Classdefinition import PHOTOSENSOR_reading

# Initialisieren des Objekts
photosensor = PHOTOSENSOR_reading()

# Bestimmen der aktuellen Messwerte der Wellenlängen
photosensor.read_channels()

# Debugging Ausgabe der Messwerte der Wellenlängen
print(f"Messwerte erfolgreich ausgelesen: {photosensor.channel_data}")

# Bestimmen der aktuellen Algenkonzentration
photosensor.get_algae_concentration()

# Debugging Ausgabe der Algenkonzentration
print(f"Aktuelle Algenkonzentration erfolgreich bestimmt: {photosensor.algae_concentration}")