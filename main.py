import json
import os
import socket
import time
from datetime import datetime
from time import sleep

import paho.mqtt.client as mqtt_client
from dotenv import load_dotenv
from paho.mqtt import MQTTException

load_dotenv()

broker = os.getenv("MQTT_IP")
port = int(os.getenv("MQTT_PORT"))
topic = "home/sensor/weather_station"

IS_DEBUG = os.getenv("DEBUG", default='true').lower() in ['true', '1', 'yes']
LOG_TO_CONSOLE = os.getenv("LOG_TO_CONSOLE", default='true').lower() in ['true', '1', 'yes']
LOG_FILE = os.getenv("LOG_FILE", default='./default_log.txt')

MAX_RECONNECT_ATTEMPTS = int(os.getenv("MAX_RECONNECT_ATTEMPTS", default=5))
INFINITE_LOOP = os.getenv("INFINITE_LOOP", default='false').lower() in ['true', '1', 'yes']
MESSAGE_INTERVAL = int(os.getenv("MESSAGE_INTERVAL", default=3))

TEMPERATURE_FILE = os.getenv("TEMPERATURE_FILE", default=None)
HUMIDITY_FILE = os.getenv("HUMIDITY_FILE", default=None)
AIR_QUALITY_FILE = os.getenv("AIR_QUALITY_FILE", default=None)
TVOC_FILE = os.getenv("TVOC_FILE", default=None)
ECO2_FILE = os.getenv("ECO2_FILE", default=None)

FILE_PATHS = [TEMPERATURE_FILE, HUMIDITY_FILE, AIR_QUALITY_FILE, TVOC_FILE, ECO2_FILE]


def print_message(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    message = f"[{timestamp}] {message}"

    if LOG_TO_CONSOLE:
        print(message)

    else:
        with open(LOG_FILE, 'a') as file:
            file.write(message + '\n')
            file.flush()  # Force immediate write to the file
            os.fsync(file.fileno())  # Ensure the OS writes the changes to disk


def log_message(message):
    if IS_DEBUG:
        print_message(f"LOG: {message}")


def error_message(message):
    print_message(f"ERROR: {message}")


def connect_mqtt():
    log_message(f'Connecting to MQTT broker at {broker}:{port}...')

    global IS_CONNECTED
    global MAX_RECONNECT_ATTEMPTS

    while MAX_RECONNECT_ATTEMPTS > 0:
        try:
            client = mqtt_client.Client(
                callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)
            client.connect(broker, port)

            log_message("Connected to MQTT broker successfully!")

            return client

        except (MQTTException, ConnectionRefusedError, socket.error) as e:
            MAX_RECONNECT_ATTEMPTS -= 1
            log_message(f"Failed to connect to broker: {e}")

        except Exception as e:
            MAX_RECONNECT_ATTEMPTS -= 1
            log_message(f"Unexpected error: {e}")

        log_message(f"Remaining attempts: {MAX_RECONNECT_ATTEMPTS}")
        sleep(2)

    error_message("Failed to connect to MQTT broker and maximum reconnection attempts reached. Exiting.")
    exit(1)


def publish_message(client, message):
    result = client.publish(topic, message)
    status = result[0]

    if status == 0:
        log_message(f"Message `{message}` sent to topic `{topic}`")
    else:
        error_message(f"Failed to send message to topic `{topic}`")


def read_values_from_files():
    values = []

    for file_path in FILE_PATHS:
        try:
            with open(file_path, 'r') as file:
                content = file.read().strip()

                number = float(content) if '.' in content else int(content)
                values.append(number)
        except (ValueError, FileNotFoundError, IOError) as e:
            error_message(f"Error reading {file_path}: {e}")
            values.append(None)

    return values


def main():
    client = connect_mqtt()
    client.loop_start()

    while True:
        values = read_values_from_files()

        message = {"temperature": values[0],
                   "humidity": values[1],
                   "air_quality": values[2],
                   "tvoc": values[3],
                   "eco2": values[4]}

        publish_message(client, json.dumps(message))

        if not INFINITE_LOOP:
            break

        time.sleep(MESSAGE_INTERVAL)

    client.loop_stop()
    log_message("Program exited.")


if __name__ == "__main__":
    main()
