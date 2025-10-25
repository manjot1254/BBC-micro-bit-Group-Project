import serial
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import json
import statistics
import time

# GLOBAL DICTIONARY #
msg_dict = {
    'sender_id': 'x',
    'receiver_id': 'x',
    'temp': [],
    'humidity': [],
    'run_time': [],
    'light_level': [],
    'steps': [],
    'meters': [],
    'speed': []
}

# Color codes for terminal text
GREEN = "\033[1;32;40m"
GRAY = "\033[0;37;40m"

# Initialize the serial connection to the MicroBit
connection = serial.Serial(port='/dev/tty.usbmodem1202', baudrate=115200, timeout=1)

# Personal ID
personal_id = 'nnvv5463'

# Command to change target
def change_target(new_target):
    global msg_dict
    msg_dict['receiver_id'] = new_target

# Validate the structure of an incoming message
def validate_message(message_dict):
    expected_keys = ['sender_id', 'receiver_id', 'temp', 'humidity', 'run_time', 'light_level', 'steps', 'meters', 'speed']
    for key in expected_keys:
        if key not in message_dict:
            return False
    return True

# List to store unseen messages
inbox = []

# Update the global dictionary with new values
def add_value(message):
    global msg_dict
    start_time = time.time()
    for i in range(5):
        msg_dict['temp'].append(message['temp'])
        msg_dict['humidity'].append(message['humidity'])
        msg_dict['run_time'].append(round(time.time() - start_time))
        msg_dict['light_level'].append(message['light_level'])
        msg_dict['steps'].append(message['steps'])
        msg_dict['meters'].append(message['meters'])
        msg_dict['speed'].append(message['speed'])
        time.sleep(1)
    return msg_dict

# Receive and process messages from the serial connection
def receive_message():
    global inbox
    try:
        if connection.in_waiting > 0:
            message = connection.readline().decode().strip()
            try:
                # Parse the received message
                received_data = json.loads(message)
                add_value(received_data)

                # Add to inbox if the message is valid and for this device
                if validate_message(msg_dict) and msg_dict['receiver_id'] == personal_id:
                    print(f"{GREEN}{msg_dict}{GRAY}")
                    inbox.append(msg_dict)
            except json.JSONDecodeError:
                print(f"{GRAY}Invalid message format: {message}{GRAY}")
    except Exception as e:
        print(f"Error receiving message: {e}")

# Display all messages in the inbox
def show_inbox():
    if inbox:
        print(f"{GREEN}--- INBOX ---{GRAY}")
        for msg in inbox:
            print(f"{GREEN}{msg}{GRAY}")
        inbox.clear()  # Clear the inbox after showing messages
        print(f"{GREEN}--- END OF INBOX ---{GRAY}")
    else:
        print(f"{GREEN}Your inbox is empty.{GRAY}")

# Analyze the received data
def analyze_data(data):
    speed_values = data['speed']
    temperature_values = data['temp']

    average_speed = statistics.mean(speed_values)
    highest_speed = max(speed_values)
    fluctuation_range = highest_speed - average_speed

    average_temperature = statistics.mean(temperature_values)
    highest_temperature = max(temperature_values)

    return {
        "averageSpeed": round(average_speed, 1),
        "highestSpeed": round(highest_speed, 1),
        "fluctuationRange": round(fluctuation_range, 1),
        "averageTemperature": round(average_temperature, 1),
        "highestTemperature": round(highest_temperature, 1)
    }

# Plot speed over time
def plot_speed_over_time(data):
    plt.figure()
    plt.plot(data['run_time'], data['speed'], marker='o', label='Speed (m/s)')
    plt.xlabel('Time (s)')
    plt.ylabel('Speed (m/s)')
    plt.title('Speed Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()

# Plot temperature over time
def plot_temperature_over_time(data):
    plt.figure()
    plt.plot(data['run_time'], data['temp'], color='orange', marker='o', label='Temperature (°C)')
    plt.xlabel('Time (s)')
    plt.ylabel('Temperature (°C)')
    plt.title('Temperature Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()

# Plot bar chart for steps, meters, and light levels
def plot_bar_chart(data):
    plt.figure()
    bar_width = 0.3
    x_indices = range(len(data['run_time']))

    plt.bar([x - bar_width for x in x_indices], data['steps'], width=bar_width, label='Steps')
    plt.bar(x_indices, data['meters'], width=bar_width, label='Meters')
    plt.bar([x + bar_width for x in x_indices], data['light_level'], width=bar_width, label='Light Level')

    plt.xlabel('Time (s)')
    plt.ylabel('Values')
    plt.title('Comparison of Steps, Meters, and Light Levels')
    plt.xticks(ticks=x_indices, labels=data['run_time'])
    plt.legend()
    plt.grid(True)
    plt.show()

# Plot and analyze the data
def analyze_and_plot(data):
    analysis_results = analyze_data(data)
    print(f"{GREEN}Analysis Results:{GRAY}", analysis_results)

    plot_speed_over_time(data)
    plot_temperature_over_time(data)
    plot_bar_chart(data)


def main():
    try:
        while True:
            # Check for incoming messages
            receive_message()

            # Allow the user to view their inbox
            show_inbox()

            # Analyze and plot data periodically (or based on user input)
            analyze_and_plot(msg_dict)

            # Ask the user for a command to either exit or continue
            user_input = input(f"{GREEN}Type 'exit' to quit or press Enter to continue: {GRAY}")
            if user_input.lower() == 'exit':
                print(f"{GREEN}Exiting program...{GRAY}")
                break

    except KeyboardInterrupt:
        print(f"\n{GREEN}Program interrupted by user. Exiting...{GRAY}")
    finally:
        if connection.is_open:
            connection.close()
            print(f"{GREEN}Serial connection closed.{GRAY}")

if __name__ == "__main__":
    main()
