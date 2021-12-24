from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps

# ---------- FREE API KEY examples ---------------------

owm = OWM('API Key here')
mgr = owm.weather_manager()


# Search for current weather in Minneapolis and get details

weather = mgr.weather_at_place('Minneapolis,US').weather
temp_dict_fahrenheit = weather.temperature('fahrenheit')  # a dict in Fahrenheit units
print("The temp is" + str(temp_dict_fahrenheit))
