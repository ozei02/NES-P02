import time
import board
import busio
import adafruit_vl6180x
# Create I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)
# Create sensor instance.
tof = adafruit_vl6180x.VL6180X(i2c)
# Main loop prints the range and lux every second:
while True:
# Read the range in millimeters and print it.
range_mm = tof.range

