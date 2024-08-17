# Code to connect to the Adafruit BME280 breakout board that records temperature, humidity, and barometric pressure
# https://www.adafruit.com/product/2652

import board
import time
from adafruit_bme280 import basic as adafruit_bme280

# Create sensor object, using the board's default I2C bus.
i2c = board.I2C()   # uses board.SCL and board.SDA
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

# change this to match the location's pressure (hPa) at sea level
bme280.sea_level_pressure = 1120.25 #1013.25

def C_to_F(C:float)->float:
    return (C * 9/5) + 32.


while True:
    print("\nTemperature: %0.1f F" % C_to_F(bme280.temperature))
    print("Humidity: %0.1f %%" % bme280.relative_humidity)
    print("Pressure: %0.1f hPa" % bme280.pressure)
    print("Altitude = %0.2f meters" % bme280.altitude)
    time.sleep(2)