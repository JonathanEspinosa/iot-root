import string
from iot.vo.sonoff import SonoffVO
from django.http.response import JsonResponse
from rest_framework.fields import empty
from iot.mqtt import mqtt
from iot.serializer.deviceSerializer import DeviceSerializer
from iot.models import Device
from iot.models.Type import Type
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
import jsonpickle
import time
import json


class TypeListView(ListAPIView):
    serializer_class = DeviceSerializer
    permission_classes = ()
    queryset = Type.objects.all()

# aumentar el topic para q pueda acceder segun el nombre
class OnoffApiView(APIView):
    

    def get(self, request, format=None, name=''):
        # Defines topic a escuchar
        #cadena = {{ "tele/"|add:'casa'}},
        #mqtt.subscribeTopic = {{ cadena |add:"/STATE" }} 
        mqtt.subscribeTopic = "tele/"+ name +"/STATE"
        
 
        # Declaras la suscripcion para estar en escucha
        # SIEMPRE USAR mqtt.subscribeTopic
        mqtt.client.subscribe(mqtt.subscribeTopic)

        # Mandas a solicitar la informacion al sonoff
        mqtt.client.publish("cmnd/"+ name +"/POWER", "TOGGLE")

        # validas si la variable global tiene o no respuesta
        validation = mqtt.globalResponse is None if True else False
        error = False
        count = 0

        # defines VO para manipular los datos
        response = SonoffVO()

        # Ciclo para esperar respuesta mqtt
        # 3 oportunidades de 1 seg
        # En cada oportunidad ejecuta la llamada de nuevo
        # Si en las 3 oportunidades no hay respuesta, corta proceso y manda error
        while validation:
            count += 1
            if count == 3:
                error = True
                validation = False

            if not error:
                time.sleep(1)
                if mqtt.globalResponse is None:
                    mqtt.client.publish("cmnd/"+ name +"/POWER", "TOGGLE")
                else:
                    validation = False
                    # Transformacion de JSON a VO del tipo Sonoff

                    response = SonoffVO(mqtt.globalResponse)
                    print("la respuesta esta aqui", response.POWER)
    


                    # Liberacion de variable de respuesta global
                    mqtt.globalResponse = None

        # Ejemplo de manipulacion de datos JSON recibidos
        response.Sleep =  "MODIFICACION 1ER NIVEL"
        response.Wifi.AP = "MODIFICACION 2DO NIVEL"

        # Validacion si presenta un error de respuesta
        if error:

            return Response({"Error": "No se encontro respuesta del dispositivo"})
        else:
            # Uso de libreria externa jsonpickle para transformar objeto VO en JSON retornarlo
            return Response(json.loads(jsonpickle.encode(response)))
