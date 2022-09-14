import traceback
import logging
import time
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
from datetime import datetime

# Initilize owm
owm = OWM('cc98066d355099341267dd7559c5f6b0')
mgr = owm.weather_manager()

# Search for current weather in Minneapolis and get details
one_call = mgr.one_call(lat=44.980, lon=-93.264, exclude='minutely,hourly', units='imperial')

# Set weather values
humidity = float(one_call.current.humidity) 
tempdic = one_call.current.temperature()
tempf = tempdic["temp"]

print(tempf)
print(humidity)