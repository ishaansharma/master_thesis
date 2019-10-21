import paho.mqtt.client as pahoClient
import time
import traceback
from paho.mqtt.client import WebsocketConnectionError
import uuid

'''
This program extracts the AIS data from digitraffic.fi. 
'''

server = 'meri-aws-mqtt-test.digitraffic.fi'
port = 80
username = 'digitraffic'
password = 'digitrafficPassword'

ais_PositionalFile = 'PositionData.txt'  # for Types 1, 2 and 3: Position Report Class A data
ais_VoyageFile = 'VoyageData.txt'  # for Type 5: Static and Voyage Related Data
Connected = False


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        global Connected
        Connected = True

    else:
        print("No data received from  {0} !".format(server))


def on_subscribe(client, userdata, mid, granted_qos):
    pass


def on_message(client, userdata, message):
    data_message = str(message.payload.decode('utf-8'))

    # these are known bad strings coming frequently from server
    if (not "CONNECTED" in data_message) and (not 'DISCONNECTED' in data_message) and (not '>{' in data_message):

        # Types 1, 2 and 3: Position Report Class A data
        if not "referencePointA" in data_message:
            with open(ais_PositionalFile, 'a') as aisPositionalData:
                aisPositionalData.write(data_message)

        # Type 5: Static and Voyage Related Data
        if not "heading" in data_message:
            with open(ais_VoyageFile, 'a') as aisVoyageData:
                aisVoyageData.write(data_message)


def start_dataCollector():
    try:
        clientId = str(uuid.uuid4())
        topic = 'vessels/#'
        Client = pahoClient.Client(clientId, transport='websockets')
        Client.username_pw_set(username, password)
        Client.on_connect = on_connect
        Client.on_message = on_message
        Client.on_subscribe = on_subscribe

        Client.connect(server, port)
        Client.subscribe(topic, 1)
        Client.loop_forever()
        

    except WebsocketConnectionError :
        print("WebSocket Connection error occurred. Error Message: " + traceback.format_exc())

    except TimeoutError :
        print("TimeOut error Occurred. Error Message: " + traceback.format_exc())

    except ConnectionRefusedError:
        print("Connection Refused. Error Message: " + traceback.format_exc())

    # if some general error occurred
    except Exception:
        print(traceback.format_exc())


start_dataCollector()