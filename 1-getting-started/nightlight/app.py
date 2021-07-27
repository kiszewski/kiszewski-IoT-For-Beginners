import time
import json
import paho.mqtt.client as mqtt

from counterfit_connection import CounterFitConnection
from counterfit_shims_grove.grove_light_sensor_v1_2 import GroveLightSensor
from counterfit_shims_grove.grove_led import GroveLed
from configs import *  

CounterFitConnection.init('127.0.0.1', 5000)

light_sensor = GroveLightSensor(0)
led_actuador = GroveLed(1)

client_name = id + 'nightlight_client'
mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')

mqtt_client.loop_start()

def handle_command(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Message received:", payload)

    if payload['led_on']:
        led_actuador.on()
    else:
        led_actuador.off()

mqtt_client.subscribe(server_command_topic)
mqtt_client.on_message = handle_command

while True:
    light_state = light_sensor.light
    telemetry_json = json.dumps({'light': light_state})

    mqtt_client.publish(client_telemetry_topic, telemetry_json)
    print("Telemetry sent ", telemetry_json)
    time.sleep(5)

# while True:
#     light = light_sensor.light

#     if light > 512:
#         led_actuador.on()
#         time.sleep(1)
#     else:
#         led_actuador.off()
#         print('Light level:', light)
#         time.sleep(1)