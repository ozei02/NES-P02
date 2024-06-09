# Klasse zum zentralen abspeichern aller Parameter

class parameters:

    # Versuchsparameter

    # Dateinamen für Messdateien
    filename_dark = "Messreihe4_dark_BP24.csv"
    filename_bright = "Messreihe4_bright_BP24.csv"
    
    # Gesamtversuchszeit
    runtime = 60*60*24*14 # Gesamtversuchszeit/s

    # Steuerparameter der Lampen
    lamps_on_time       = 60*60*24*7 # 24/7 an
    lamps_off_time      = 0 # 0 Stunden

    # Steuerparameter der Luftpumpe
    airpump_on_time     = 60*15 # 15 Minuten
    airpump_off_time    = 60*15 # 15 Miuten

    # Volumen des Düngers das pro Tag in den Reaktor gegeben werden soll
    V_fertilization = 100 # ml/d

    # Abtastzeit der Messungen
    sampletime_measurements = 60*30 # 30 Minuten

    # Abtastzeit der Kamera
    sampletime_cam = 60*60*1 # 1 Stunde

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
    fertilizerpump_pin = 25
    