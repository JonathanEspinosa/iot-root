from iot.mqtt import mqtt
from iot.serializer.typeSerializer import TypeSerializer
from iot.models.Type import Type
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response


class TypeListView(ListAPIView):
    # def mqtt():
    mqtt.client.subscribe("tele/casa/STATE")
    mqtt.client.publish("cmnd/casa/POWER", "TOGGLE")
    # while mqtt.response=='':
    mqtt.client.publish("cmnd/casa/POWER", "TOGGLE")
    print(mqtt.response)
    print(mqtt.client.on_message)
    print(mqtt.response)

    
    serializer_class = TypeSerializer
    permission_classes = ()
    queryset = Type.objects.all()
    # mqtt()


class testApiView(APIView):
    def get(self, request, format=None):
        mqtt.client.publish("cmnd/casa/POWER", "TOGGLE")
        # def mqtt():
        #     client.publish("cmnd/jeem/POWER", "TOGGLE")
        #     return 'entroooo'
        # mqtt()
        an_apiview = ["asdasdasdsadas", "asdasdasdsadas"]

        return Response({"message": "Hello", "an_apiview": an_apiview})
