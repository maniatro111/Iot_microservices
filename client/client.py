import paho.mqtt.client as mqtt

from sys import argv
from json import dumps
from random import choice
from time import sleep


if __name__ == "__main__":

    if len(argv) < 2:
        print("Usage:\npython3 client.py <location>")
        exit(0)

    posibilities = {
            'UPB':{
                'stations': ['Gas', 'Mongo', 'RPi_1']
                },
            'Dorinel':{
                'stations': ['Zeus', 'Hermes', 'Poseidon']
                },
            'Florinel':{
                'stations': ['Kratos', 'Atreus', 'Odin']
                }
            }
    if argv[1] not in list(posibilities.keys()):
        print(f'Unknown location.\nKnown locations: {posibilities.keys()}')
        exit(0)

    client = mqtt.Client()
    try:
        client.connect("localhost")
    except:
        print("No broker on port 1883.")
        exit(0)

    client.loop_start()

    batts = list(range(80, 101))
    temps = list(range(20, 41))
    humids = list(range(20, 41))
    times = list(range(1, 4))
    generate_string = list(range(0, 2))

    while True:
        iot_data = {
                'BAT': choice(batts),
                'TEMP': choice(temps),
                'HUMID': choice(humids),
        }
        if choice(generate_string) == 1:
            iot_data['status'] = 'ok'

        if choice(generate_string) == 1:
            iot_data['timestamp'] = '2023-01-01T20:35:57'

        station = choice(posibilities[argv[1]]['stations'])
        client.publish(f'{argv[1]}/{station}', dumps(iot_data))
        print(f'Station {station} published:\n{dumps(iot_data, indent=4)}\n')

        sleep(choice(times) * 60)
