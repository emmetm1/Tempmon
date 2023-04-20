import os
import logging
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import influxdb_client
import adafruit_dht
import board
import time
from dotenv import load_dotenv

load_dotenv()
token = os.environ["API_TOKEN"]

logging.basicConfig(
    filename='/var/log/tempmon.log', level=logging.ERROR,
    format='%(asctime)s %(levelname)s %(name)s %(message)s'
)

org = "whem-home"
bucket = "Weather-Data"
dht = adafruit_dht.DHT22(board.D4)
INFLUXDB_SERVER_URL = "http://192.168.50.66:8086"
SLEEP_INTERVAL = 180

def read_sensor_data(max_retries=5):
    for _ in range(max_retries):
        try:
            temp_c = dht.temperature
            humidity = dht.humidity
            return temp_c, humidity
        except RuntimeError as e:
            logging.warning(f"RuntimeError: {e}. Retrying...")
            time.sleep(2)
    logging.error("Failed to read sensor data after {} attempts.".format(max_retries))
    return None, None

def main():
    with InfluxDBClient(url=INFLUXDB_SERVER_URL, token=token, org=org) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)
        last_read_time = time.monotonic()

        while True:
            current_time = time.monotonic()

            if current_time - last_read_time >= SLEEP_INTERVAL:
                temp_c, humidity = read_sensor_data()

                if temp_c is not None and humidity is not None and -40 <= temp_c <= 125 and 0 <= humidity <= 100:
                    temp_f = temp_c * 9.0 / 5.0 + 32.0
                    TempData = Point("Temp").tag("location", "Upstairs").field("temp_f", temp_f).time(datetime.utcnow(), WritePrecision.NS)
                    HumidityData = Point("Humidity").tag("location", "Upstairs").field("humidity", humidity).time(datetime.utcnow(), WritePrecision.NS)
                    write_api.write(bucket, org, TempData)
                    write_api.write(bucket, org, HumidityData)
                    last_read_time = current_time
                else:
                    logging.warning("Invalid sensor data: temperature=%s, humidity=%s", temp_c, humidity)
            time.sleep(1)

if __name__ == "__main__":
    main()
