from microbit import *

# Microbit radio
import radio

# Configure the radio
radio.config(channel=10, group=9)
radio.on()

# Initlises UART with the default settings
uart.init(baudrate=115200)

# Microbit ID
personal_id = 'nnvv5462'

while True:

    # Receive messages
    incoming = radio.receive()
    if incoming:
        display.scroll(incoming)
        uart.write(incoming)

