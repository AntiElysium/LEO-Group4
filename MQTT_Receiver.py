import paho.mqtt.client as mqtt
import csv
import time
from datetime import datetime

mqttBroker = "broker.mqttdashboard.com"

def write_to_file(message):
    data = message.split(',')
    dt = datetime.now()
    timestamp = datetime.timestamp(dt)

    with open("dataFile.csv", "a") as csvfile:
        csvwriter = csv.writer(csvfile)

        # CO2
        csvwriter.writerow([timestamp, 'co2', data[0], 'ppm'])
        # Temperature
        csvwriter.writerow([timestamp, 'temp', data[1], 'C'])
        # Humidity
        csvwriter.writerow([timestamp, 'humid', data[2], 'g/m3'])

# https://medium.com/python-point/mqtt-basics-with-python-examples-7c758e605d4
def on_message(client, data, message):
    decodedMessage = str(message.payload.decode("utf-8"))
    print("Message: " , decodedMessage)
    write_to_file(decodedMessage)

client = mqtt.Client("Python_Server")
client.connect(mqttBroker)

client.loop_start()

client.subscribe("big_bouncing_inflatable_green_ball")
client.on_message=on_message

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("exiting")
    client.disconnect()
    client.loop_stop()


# time.sleep(30)
# client.loop_stop()
