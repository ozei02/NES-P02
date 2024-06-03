from PHOTOSENSOR_Classdefinition import PHOTOSENSOR_control

# Initialisieren des Objekts
photosensor = PHOTOSENSOR_control()

# Bestimmen der aktuellen Algenkonzentration
algae_concentration_current = photosensor.get_sensor_value_at_clear()