import traceback
import logging
import time
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
from datetime import datetime
import influxdb_client
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


# Initilize owm
owm = OWM('cc98066d355099341267dd7559c5f6b0')
mgr = owm.weather_manager()

# Initilize Influx Client
token = "Gtvnbd9_wl5bf52mPfXCVc-ERnbEGMMTRscK_fhwQqnoL1V58sJpsjW42gDhQh2ANIV_GCZoTsAcMXV5pLSm4A=="
org = "whem-home"
bucket = "Weather-Data"
client = influxdb_client.InfluxDBClient(url="http://192.168.50.66:8086", token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)



# Test prints to confirm values
#print("temp is " + str(temp_f))
#print("humidity is " + str(humid))


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
