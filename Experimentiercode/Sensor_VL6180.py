import time
import board
import busio
import adafruit_vl6180x
import RPi.GPIO as GPIO

# Set up GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)

# Define the BCM pin numbers for SCL and SDA
SCL_PIN = 3  # BCM pin for SCL (I2C1_SCL)
SDA_PIN = 2  # BCM pin for SDA (I2C1_SDA)

# Create I2C bus using BCM pin numbers.
i2c = busio.I2C(SCL_PIN, SDA_PIN)

# Create sensor instance.
tof = adafruit_vl6180x.VL6180X(i2c)

# Main loop prints the range and lux every second:
while True:
    try:
        # Read the range in millimeters and print it.
        range_mm = tof.range
        print(f"Range: {range_mm} mm")

        # Optionally, read the lux (ambient light level) and print it.
        lux = tof.read_lux(adafruit_vl6180x.ALS_GAIN_1)
        print(f"Lux: {lux} lux")

        # Wait for a second before the next reading.
        time.sleep(1)
    except RuntimeError as e:
        print(f"RuntimeError: {e}")
        # Optionally, add a small delay to avoid spamming error messages.
        time.sleep(0.1)
    except Exception as e:
        print(f"Exception: {e}")
        # Breaking out of the loop in case of unexpected errors.
        break
