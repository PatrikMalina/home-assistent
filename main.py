import os

import paho.mqtt.client as mqtt_client
from dotenv import load_dotenv

load_dotenv()

broker = os.getenv("MQTT_IP")
port = int(os.getenv("MQTT_PORT"))
topic = "home/sensor/temperature"  # MQTT topic


def connect_mqtt():
    client = mqtt_client.Client(callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)
    client.connect(broker, port)
    return client


def main():
    client = connect_mqtt()


if __name__ == "__main__":
    main()
