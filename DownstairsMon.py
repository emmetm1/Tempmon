from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import influxdb_client
import adafruit_dht
import board
import time
import os
from dotenv import load_dotenv
import logging

log_file = '/var/log/tempmon.log'
logging.basicConfig(filename=log_file, level=logging.DEBUG)

# load env variables
load_dotenv()

# Initilize DHT22
dht = adafruit_dht.DHT22(board.D4)

# Initilize Influx Client
token = os.getenv("INFLUX_API_KEY")
org = "whem-home"
bucket = "Weather-Data"
location = "Downstairs"
client = influxdb_client.InfluxDBClient(url="http://192.168.50.66:8086", token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

while True:
    try:
        temp_c = dht.temperature
        humidity = dht.humidity
        temp_f = temp_c * 9.0 / 5.0 + 32.0

        if humidity is None or temp_c is None:
            raise Exception("Failed to read from DHT22 sensor")
        if humidity > 100 or humidity < 0 or temp_f < -40 or temp_f > 120:
            raise Exception("Invalid data received from DHT22 sensor")

        TempData = Point("Temp").tag("location", location).field("temp_f", temp_f).time(datetime.utcnow(), WritePrecision.NS)
        HumidityData = Point("Humidity").tag("location", location).field("humidity", humidity).time(datetime.utcnow(), WritePrecision.NS)
        write_api.write(bucket, org, TempData)
        write_api.write(bucket, org, HumidityData)
        
        logging.info("write to db success. temp_f %s, humidity %s", temp_f, humidity)
        time.sleep(300)
    except Exception as e:
        logging.error("Error while reading from sensor: %s", e)
        time.sleep(10)