from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import influxdb_client
import adafruit_dht
import board
import time
import os
from dotenv import load_dotenv

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

        TempData = Point("Temp").tag("location", location).field("temp_f", temp_f).time(datetime.utcnow(), WritePrecision.NS)
        HumidityData = Point("Humidity").tag("location", location).field("humidity", humidity).time(datetime.utcnow(), WritePrecision.NS)
        write_api.write(bucket, org, TempData)
        write_api.write(bucket, org, HumidityData)
        
        print("write to db success", temp_f)
        time.sleep(300)
    except RuntimeError as e:
        continue
