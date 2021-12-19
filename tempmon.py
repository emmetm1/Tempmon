import time

import adafruit_dht
import board

dht = adafruit_dht.DHT22(board.D4)

while True:
    try:
        temp_c = dht.temperature
        humidity = dht.humidity
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        # Print what we got to the REPL
        print("Temp: {:.1f} *F \t Humidity: {}%".format(temp_f, humidity))
    except RuntimeError as e:
        # Reading doesn't always work! Just print error and we'll try again
        print("Reading from DHT failure: ", e.args)

    time.sleep(1)
