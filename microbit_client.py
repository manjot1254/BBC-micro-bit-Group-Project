from microbit import *

# Microbit radio
import radio
from bme688 import *
from OLED import *
from microbit import *
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd

class all_data:
    def __init__(self):
        self.steps = 0
        self.meter = 0.0
        self.light_level = ''

data = all_data()

# Configure the radio
radio.config(channel=10, group=9)
radio.on()

# Initlises UART with the default settings
uart.init(baudrate=115200)

# Microbit IDs
personal_id = "mll22rma"
receiver_id = "nnvv5463"

def create_message(key, value):
    message = {key: value}
    return message

while True:
    if accelerometer.was_gesture('shake'):
        data.steps += 1
        data.meter = data.steps * 0.8

    if display.read_light_level() > 50:
        data.light_level = 'Day'
    else:
        data.light_level = 'Night'
    read_data_registers()
    temp = calc_temperature()
    humidity = calc_humidity()
    pressure = calc_pressure()
    iaqScore, iaqPercent, eCO2Value = calc_air_quality()

    run_time=running_time()//1000
    show("Temperature: {} C".format(temp), 0)
    show("Humidity: {} %".format(humidity), 1)
    show("eCO2 Value: {}".format(eCO2Value) + " ppm", 2)
    show("running time: {}".format(run_time)+" S",3)
    show("Light level: {}".format(data.light_level),4)
    show("Steps: {}".format(data.steps),5)
    show("Meter: {}".format(data.meter),6)
    show("Speed: {}".format(data.meter/run_time)+" m/s",7)

    # Send a message when button B is pressed
    if button_b.was_pressed():
        radio.send(str({'sender_id': personal_id}))
        radio.send(str({'receiver_id': receiver_id}))
        radio.send(str({'temp': temp}))
        radio.send(str({'humidity': humidity}))
        radio.send(str({'run_time': run_time}))
        radio.send(str({'light_level': data.light_level}))
        radio.send(str({'steps': data.steps}))
        radio.send(str({'meters': data.meter}))
        radio.send(str({'speed': data.meter/run_time,}))
             # Values unknown but can be formatted similarly

    sleep(500)
