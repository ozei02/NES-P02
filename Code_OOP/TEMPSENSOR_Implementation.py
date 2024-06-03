from TEMPSENSOR_Classdefinition import TEMPSENSOR_control

# Initialisieren des Objekts
T_sensor = TEMPSENSOR_control()

# Messen der aktuellen Temperatur
T_current = T_sensor.tempC(0)