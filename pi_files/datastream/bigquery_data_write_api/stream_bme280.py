# Run in background with: nohup python stream_bme280.py &
# Or to not include the output log file: nohup python stream_bme280.py > /dev/null 2>&1&
from append_rows import bigquery_storage_v1, create_row_bme280, send_rows_to_bq
from adafruit_bme280 import basic as adafruit_bme280
import board
import time

if __name__ == '__main__':    

    # Initialize the bigquery client
    write_client = bigquery_storage_v1.BigQueryWriteClient()

    # Create sensor object, using the board's default I2C bus.
    i2c = board.I2C()   # uses board.SCL and board.SDA
    bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

    # change this to match the location's pressure (hPa) at sea level
    bme280.sea_level_pressure = 1120.25 #1013.25

    def C_to_F(C:float)->float:
        return (C * 9/5) + 32.
    
    while True:

        rows = [
            create_row_bme280('Home', '1', C_to_F(bme280.temperature), bme280.relative_humidity, bme280.pressure)
        ]
        # print(rows)
        send_rows_to_bq("smart-beehive-431213", "sensor_data", "bme280", write_client, rows)
        time.sleep(1)