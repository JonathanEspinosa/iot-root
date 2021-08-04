import string
from paho.mqtt import client as mqtt_client

broker = "3.140.85.3"
port = 1883
topic = "cmnd/casa/POWER"
topic1 = "tele/casa/STATE"
# username = 'emqx'
# password = 'public'
client = mqtt_client.Client()
response: str=''


class Mqtt:
    def connect_mqtt():
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        def on_message(client, userdata, msg):
            if msg.topic == "tele/casa/STATE":
                print( str(msg.payload))

        # Set Connecting Client ID
        # client.username_pw_set(username, password)
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(broker, port)
        return client

    # def publish():
    #     msg = 'TOGGLE'
    #     res = client.publish(topic, msg)
    #     if res[0] == 0:
    #         print(f"Send `{msg}` to topic `{topic}`")
    #     else:
    #         print(f"Failed to send message to topic {topic}")


# def on_connect(client, userdata, flags, rc):
#     print("Se conecto con mqtt " + str(rc))
#     client.subscribe("tasmota")
#     client.subscribe("jeem")
#     client.subscribe("tele/jeem/STATE")


# def on_message(client, userdata, msg):
#     # def switch_demo(argument): print(msg.topic + " " + str(msg.payload))
#   print(msg.topic + " " + str(msg.payload))
#     # if msg.topic == "prueba":
#     # if msg.topic == "jona":
#         # print(str(msg.payload))
#     # print(msg.topic + " " + str(msg.payload))


# client = mqtt.Client()
# client.on_connect = on_connect
# client.on_message = on_message

# client.connect("192.168.100.6", 1883, 3) #cada cuanto se intenta reconectar
# client.loop_forever()
