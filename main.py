import json
import os
import random
import time

import paho.mqtt.client as mqtt_client
from dotenv import load_dotenv

load_dotenv()

broker = os.getenv("MQTT_IP")
port = int(os.getenv("MQTT_PORT"))
topic = "home/sensor/weather_station"  # MQTT topic


def connect_mqtt():
    client = mqtt_client.Client(
        callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)
    client.connect(broker, port)
    return client


def publish_message(client, message):
    result = client.publish(topic, message)
    status = result[0]
    if status == 0:
        print(f"Message `{message}` sent to topic `{topic}`")
    else:
        print(f"Failed to send message to topic `{topic}`")


def main():
    client = connect_mqtt()
    client.loop_start()

    i = 0
    while i < 60:
        publish_message(client,
                        json.dumps({"temperature": round(random.uniform(20.0, 30.0), 1), "humidity": random.randint(50, 100)}))
        time.sleep(1)
        i += 1

    client.loop_stop()


if __name__ == "__main__":
    main()
