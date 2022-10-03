import traceback
import logging
import time
import os
from dotenv import load_dotenv
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
from datetime import datetime

# load env variables
load_dotenv()

# Initilize owm
owm = OWM(os.getenv("OW_WEATHER_API_KEY"))
mgr = owm.weather_manager()

# Search for current weather in Minneapolis and get details
one_call = mgr.one_call(lat=44.980, lon=-93.264, exclude='minutely,hourly', units='imperial')

# Set weather values
humidity = float(one_call.current.humidity) 
tempdic = one_call.current.temperature()
tempf = float(tempdic["temp"])

print(tempf)
print(humidity)