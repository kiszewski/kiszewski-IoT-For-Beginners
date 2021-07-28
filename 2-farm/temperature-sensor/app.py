import json
import time
import paho.mqtt.client as mqtt
from configs import *
from counterfit_connection import CounterFitConnection
from counterfit_shims_seeed_python_dht import DHT

CounterFitConnection.init('127.0.0.1', 5000)
sensor = DHT("11", 5)

client_name = mqtt_id + 'temp_sensor_client'
mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')

mqtt_client.loop_start()

while True:
    humidity, temperature = sensor.read()
    print(f'Temperature {temperature}°C')
    temp_json = json.dumps({'temperature': temperature})

    mqtt_client.publish(temp_sensor_telemetry_topic, temp_json)

    time.sleep(10)