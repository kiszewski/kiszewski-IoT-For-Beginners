import json
import time
from os import path
import csv
import paho.mqtt.client as mqtt
from datetime import datetime
from configs import *

server_name = mqtt_id + 'temp_server'
mqtt_client = mqtt.Client(server_name)
mqtt_client.connect('test.mosquitto.org')
filename = 'database.csv'
fieldnames = ['date', 'temperature']

mqtt_client.loop_start()

def handle_temperature_telemetry(client, _, message):
    payload = json.loads(message.payload.decode())
    

    if not path.exists(filename):
        with open(filename, mode='w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()


    with open(filename, mode='a', newline='') as temperature_file:
        database_csv = csv.DictWriter(temperature_file, fieldnames)
        time_now = datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()

        database_csv.writerow({'date': time_now, 'temperature': payload['temperature']})
        print("Temp stored:", payload)

mqtt_client.subscribe(temp_sensor_telemetry_topic)
mqtt_client.on_message = handle_temperature_telemetry

def calculate_GDD():
    if path.exists(filename):
        with open(filename, 'r') as csv_file:
            reads = csv.DictReader(csv_file)

            days = {}
            sum_of_all_temperatures = 0.0
            counter = 1
            temperature_base = 10

            for field in reads:
                sum_of_all_temperatures = sum_of_all_temperatures + float(field['temperature'])
                cutted_date = field['date'].split('T')[0]
                
                gdd = sum_of_all_temperatures / counter - temperature_base

                days[cutted_date] = gdd

                counter += 1
            
            print(days)


while True:
    calculate_GDD()
    time.sleep(30)