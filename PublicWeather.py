import traceback
import logging
import time
import os
from dotenv import load_dotenv
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
from datetime import datetime
import influxdb_client
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# load env variables
load_dotenv()

# Initilize owm
owm = OWM(os.getenv("OW_WEATHER_API_KEY"))
mgr = owm.weather_manager()

# Initilize Influx Client
token = os.getenv("INFLUX_API_KEY")
org = "whem-home"
bucket = "Weather-Data"
client = influxdb_client.InfluxDBClient(url="http://192.168.50.66:8086", token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

while True:
    try:
        # Search for current weather in Minneapolis and get details
        one_call = mgr.one_call(lat=44.980, lon=-93.264, exclude='minutely,hourly', units='imperial')

        # Set weather values
        humidity = float(one_call.current.humidity)  
        tempdic = one_call.current.temperature()
        temp_f = tempdic["temp"]

        # Write to Influx 
        TempData = Point("Temp").tag("location", "Outdoors").field("temp_f", temp_f).time(datetime.utcnow(), WritePrecision.NS)
        HumidityData = Point("Humidity").tag("location", "Outdoors").field("humidity", humidity).time(datetime.utcnow(), WritePrecision.NS)
        write_api.write(bucket, org, TempData)
        write_api.write(bucket, org, HumidityData)
        print("write to db success", temp_f)
        time.sleep(300)
    except Exception as e:
        logging.error(traceback.format_exc())
        exit
        # Logs the error appropriately. 
