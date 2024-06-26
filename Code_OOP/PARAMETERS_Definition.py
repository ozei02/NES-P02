# Klasse zum zentralen abspeichern aller Parameter

class parameters:

    # Versuchsparameter

    # Dateinamen für Messdateien
    filename_dark = "Messreihe_dark_BP24.csv"
    filename_bright = "Messreihe_bright_BP24.csv"
    
    # Gesamtversuchszeit/s
    runtime = 60*60*24*14 

    # Steuerzeiten der Lampen/s
    lamps_on_time       = 60*2
    lamps_off_time      = 60*2 

    # Steuerzeiten der Luftpumpe/s
    airpump_on_time     = 60*2
    airpump_off_time    = 60*2 

    # Volumen des Düngers/(ml/d) 
    V_fertilization = 100 # ml/d

    # Abtastzeit der Messungen/s
    sampletime_measurements = 60*2 

    # Abtastzeit der Kamera/s
    sampletime_cam = 60*1 

    # Anzahl Messungen pro Messpunkt
    datapoints_per_measuringpoint = 5

    # Gewünschter Bereich des pH-Werts (Steuerung über CO2-Diffusoren)
    ph_max = 8.5
    ph_min = 7.5

    # Parameter für Hardware (nur bei Änderungen der Hardware und Anschlusspins am Raspberry anpassen)

    # Feste Parameter der Düngerpumpe
    fertilizerpump_dutycycle = 37 # Tastgrad je nach Versorgungsspannung der Düngepumpe und Netzteil anpassen
    fertilizerpump_startuptime = 10 # Je nach Schlauchlänge der Pumpe und der sich ergebenden Durchflutungszeit anpassen
    fertilizerpump_actiontime = 0.55 # Zeit die die Düngerpumpe zum pumpen von einem ml Flüssigkeit benötigt
    # Berechnung des Düngeintervalls anhand der geforderten Menge pro Tag
    fertilizerpump_off_time = (60*60*24/V_fertilization) # nicht ändern, wird automatisch neu berechnet

    # Anschlusspins am Raspberry
    wirelesssocket_pin_on = 27
    wirelesssocket_pin_off = 22
    lamps_pin = 17
    airpump_pin = 18
    co2gas_pin = 16
    fertilizerpump_pin = 25

    # Berechnung Anzahl Messpunkte
    datapoints_overall = runtime/sampletime_measurements # nicht ändern
    