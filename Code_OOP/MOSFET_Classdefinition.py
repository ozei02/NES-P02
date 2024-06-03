import RPi.GPIO as GPIO

# Definition einer Klasse für Objekte welche mit einem MOSFET angesteuert werden
class MOSFET_control:
    # Die __init__ Methode ist der Konstruktor der Klasse, wird also verwendet um neue Objekte hinzuzufügen
    def __init__(self, pin, tastgrad):
        self.pin = pin
        self.tastgrad = tastgrad
        self.setup()
    
    # Setup des Output Pins und der Pulsweitenmodulation (Wird bei der Initialisierung mit durchgeführt)
    def setup(self):
        GPIO.setmode(GPIO.BCM) # Konvention der Pinnummerierung (hier BCM)
        GPIO.setwarnings(False) # Warnungen, die das Ausführen des Programms verhindern, wenn Ausgang bereits als OUT deklariert wurde ignorieren
        GPIO.setup(self.pin, GPIO.OUT) # Definition des Pins als Output-Pin
        self.pwm = GPIO.PWM(self.pin, 50) # PWM mit 50Hz Frequenz initialisieren
        self.pwm.start(0) # PWM mit 0% Tastgrad starten
    
    # Methoden welche für alle per MOSFET gesteuerten Bauteile abgearbeitet werden
    # Start der Pulsweitenmodulation mit gewünschtem Tastgrad
    def start(self):
        self.pwm.ChangeDutyCycle(self.tastgrad)

    # Ende der Pulsweitenmodulation
    def stop(self):
        self.pwm.ChangeDutyCycle(0)

    # GPIO Cleanup und stoppen der PWM
    def cleanup(self):
        self.pwm.stop()
        GPIO.cleanup()
