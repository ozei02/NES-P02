from TEMPSENSOR_Classdefinition import TEMPSENSOR_reading

# Initialisieren des Objekts
T_sensor = TEMPSENSOR_reading()

# Messen der aktuellen Temperatur
T_sensor.tempC(0)

# Debugging Ausgabe zur aktuellen Temperatur
print(f"Temperatur erfolgreich gemessen: {T_sensor.tempC_current}")