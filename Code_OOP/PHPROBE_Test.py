from PHPROBE_Classdefinition import PHPROBE_reading

# Initialisieren des Objekts der pH-Sonde
ph_probe = PHPROBE_reading()

# Messen des pH-Werts
ph_probe.measure()

# Debugging Ausgabe zum aktuellen pH-Wert
print(f"pH-Wert erfolgreich gemessen: {ph_probe.ph_value}")