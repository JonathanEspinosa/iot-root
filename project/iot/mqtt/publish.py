import paho.mqtt.client as mqtt
from settingsMQTT import settings
#class publishMqtt:

   # mqtt_server = "3.140.85.3"
    #client = mqtt.Client()
    #client.connect(mqtt_server, 1883, 60)
    #def mqtt_us(self, request, topic):
     #   return "cmnd/" + topic + "/POWER"

   # def toggle():
 
light_stat = False  # Light Stat (as sent from here)


def turn_light(stat):
    """Switch ON/OFF the light"""
    global light_stat
    if stat:
        payload = "ON"
        light_stat = True
    else:
        payload = "OFF"
        light_stat = False
    client.publish(settings.light_cmd_topic, payload)
    print("Switched Light", payload)

topic = 'casa'
def on_connect(*args):
    """Callback to execute when MQTT connects"""
    print("MQTT Connected!")
    client.subscribe(settings.topic)

def on_message(*args):
    """Callback to execute when MQTT receives new message"""
    
    msg: mqtt.MQTTMessage = next(a for a in args if isinstance(a, mqtt.MQTTMessage))
    topic = msg.topic
    payload = msg.payload.decode()
    print(f"Rx @ {topic}: {payload}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

if __name__ == "__main__":
    client.connect(settings.broker, settings.port)
    
    try:
        client.loop_forever()
    except (KeyboardInterrupt, InterruptedError):
        pass
    
  
