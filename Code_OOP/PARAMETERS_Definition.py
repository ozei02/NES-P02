# Klasse zum zentralen abspeichern aller Parameter

class parameters:

    # Versuchsparameter

    # Dateinamen für Messdateien
    filename_dark = "Messreihe_dark_BP24.csv"
    filename_bright = "Messreihe_bright_BP24.csv"
    
    # Gesamtversuchszeit
    runtime = 60*60*24*14 # Gesamtversuchszeit/s

    # Steuerparameter der Lampen
    lamps_on_time       = 60*2 # 24/7 an
    lamps_off_time      = 60*2 # 0 Stunden

    # Steuerparameter der Luftpumpe
    airpump_on_time     = 60*2 # 15 Minuten
    airpump_off_time    = 60*2 # 15 Miuten

    # Steuerparameter der CO2-Diffusoren
    co2diffusor_on_time = 60*15
    co2diffusor_off_time = 60*15

    # Volumen des Düngers das pro Tag in den Reaktor gegeben werden soll
    V_fertilization = 100 # ml/d

    # Abtastzeit der Messungen
    sampletime_measurements = 60*2 # 30 Minuten

    # Abtastzeit der Kamera
    sampletime_cam = 60*60*1 # 1 Stunde

    # Anzahl Messungen pro Messpunkt
    datapoints_per_measuringpoint = 5

    # Parameter für Hardware (nur bei Änderungen der Hardware anpassen)

    # Feste Parameter der Düngerpumpe
    fertilizerpump_dutycycle = 37
    fertilizerpump_startuptime = 10
    fertilizerpump_actiontime = 0.55 # Zeit die die Düngerpumpe zum pumpen von einem ml Flüssigkeit benötigt
    # Berechnung des Düngeintervalls anhand der geforderten Menge pro Tag
    fertilizationpump_off_time = (60*60*24/V_fertilization)-fertilizerpump_actiontime 

    # Anschlusspins am Raspberry
    wirelesssocket_pin_on = 27
    wirelesssocket_pin_off = 22
    lamps_pin = 17
    airpump_pin = 18
    co2diffusor_pin = 5
    fertilizerpump_pin = 25

    # Berechnung Anzahl Messpunkte
    datapoints_overall = runtime/sampletime_measurements
    