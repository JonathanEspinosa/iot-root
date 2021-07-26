# import paho
class publishMqtt:

    ip = "3.145"

    def getTopic(name):
        return "cmnd/" + name + "/POWER"

    # def toggle():
 