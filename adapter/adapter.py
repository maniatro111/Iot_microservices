import paho.mqtt.client as mqtt
import datetime
import logging
import time
from json import loads
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from re import match
from os import getenv

def on_message(client, userdata, message):
    if not match(r'^[^/]+/[^/]+$', message.topic):
                return

    logging.debug(f'Received a message by topic [{message.topic}]') 

    locatie, statie = message.topic.split("/")

    data = loads(message.payload)

    try:
        tstamp = datetime.datetime.strptime(data['timestamp'], '%Y-%m-%dT%H:%M:%S')
        logging.debug('Data timestamp is: {}'.format(data['timestamp'].replace("T", " ")))
    except:
        tstamp = datetime.datetime.now()
        logging.debug('Data timestamp is NOW')

    write_api = userdata.write_api(write_options=SYNCHRONOUS)

    for key, val in data.items():
        if type(val) != int and type(val) != float:
            continue
        write_api.write(bucket="my-bucket", org="my-org", record={
            'measurement': f'{statie}.{key}',
            'tags': {
                'type': f'{key}',
                'statie': f'{statie}',
                'locatie': f'{locatie}'
                },
            'time': tstamp.strftime('%Y-%m-%dT%H:%M:%S'),
            'fields': {
                'Value': float(val)
                }
            })
        logging.debug(f'{locatie}.{statie}.{key} {val}')

if __name__ == "__main__":
    time.sleep(10)
    if getenv("DEBUG_DATA_FLOW") == "true":
        logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(message)s", datefmt='%Y-%m-%d %H:%M:%S')
    logging.error("Setting, Done") 
    try:
        db_comm = InfluxDBClient(url=f'http://sprc3_influxdb:8086', token="balls", org="my-org")
    except:
        print("Couldn't connect to db")

    logging.error("Connecting to Db, done")

    try:
        client = mqtt.Client("Adapter", userdata=db_comm)
        client.connect("sprc3_broker", port=1883)
        client.subscribe("#")
    except:
        print("Couldn't connect to mqtt broker.")

    logging.error("Connecting to broker. Done")
    
    client.on_message = on_message
    client.loop_forever()
