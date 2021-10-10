from paho.mqtt import client as mqtt_client
from queue import Queue

broker = "3.140.85.3"
port = 1883
subscribeTopic = None
# username = 'emqx'
# password = 'public'
client = mqtt_client.Client()
globalResponse = None


class Mqtt:
    def connect_mqtt():
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        def on_message(client, userdata, msg):
            print(subscribeTopic)
            if msg.topic == subscribeTopic:
                global globalResponse
                globalResponse = msg.payload.decode("utf8")

        # Set Connecting Client ID
        # client.username_pw_set(username, password)
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(broker, port)
        # print("=============client._bind_address===========")
        # print(client.__dict__)
        return client
