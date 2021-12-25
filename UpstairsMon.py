from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import influxdb_client
import adafruit_dht
import board
import time

# You can generate an API token from the "API Tokens Tab" in the UI
token = "Gtvnbd9_wl5bf52mPfXCVc-ERnbEGMMTRscK_fhwQqnoL1V58sJpsjW42gDhQh2ANIV_GCZoTsAcMXV5pLSm4A=="
org = "whem-home"
bucket = "Weather-Data"
dht = adafruit_dht.DHT22(board.D4)

client = influxdb_client.InfluxDBClient(url="http://192.168.50.66:8086", token=token, org=org)

write_api = client.write_api(write_options=SYNCHRONOUS)

while True:
    try:
        temp_c = dht.temperature
        humidity = dht.humidity
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        # Print what we got to the REPL
        TempData = Point("Temp").tag("location", "Upstairs").field("temp_f", temp_f).time(datetime.utcnow(), WritePrecision.NS)
        HumidityData = Point("Humidity").tag("location", "Upstairs").field("humidity", humidity).time(datetime.utcnow(), WritePrecision.NS)
        write_api.write(bucket, org, TempData)
        write_api.write(bucket, org, HumidityData)
        print("write to db success", temp_f)
        time.sleep(300)
    except RuntimeError as e:
        continue
