# Klasse zum zentralen abspeichern aller Parameter

class parameters:
    
    # Dateinamen für Messdateien
    filename_dark = "Messreihe4_dark_BP24.csv"
    filename_bright = "Messreihe4_bright_BP24.csv"
    
    # Gesamtversuchszeit
    runtime = 60*60*24*14 # Gesamtversuchszeit/s

    # Steuerparameter der Lampen
    lamps_on_time       = 60*60*24*7    # 24/7 an
    lamps_off_time      = 0             # 0 Stunden

    # Steuerparameter der Luftpumpe
    airpump_on_time     = 60*15         # 15 Minuten
    airpump_off_time    = 60*15         # 15 Miuten
    