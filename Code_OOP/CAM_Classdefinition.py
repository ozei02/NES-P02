import os
from picamera2 import Picamera2, Preview
import datetime
from time import sleep

class CAM_control:

    os.environ['LIBCAMERA_LOG_LEVELS'] = '4' # deaktiviert die Anzeige von Info/Warnings von Picamera2/Libcamera
    picam2 = Picamera2()
    camera_config = picam2.create_still_configuration(main={"size": (4608, 2592)}, lores={"size": (640, 480)}, display="lores")
    picam2.configure(camera_config)

    def __init__(self):
        pass

    def get_photo(self):
        CAM_control.picam2.start()
        now = datetime.datetime.now() # get current date and time
        date_time = now.strftime("%Y-%m-%d_%H-%M-%S")
        name = "Foto_" + date_time + ".jpg"
        sleep(2)    # Zeit für automatische Einstellung von Fokus und Belichtung
        CAM_control.picam2.capture_file(name)
        CAM_control.picam2.stop()
        date_time = now.strftime("%Y-%m-%d, %H:%M:%S") # timestamp of measurement
        print(f"{date_time}: Kamerafoto gespeichert")