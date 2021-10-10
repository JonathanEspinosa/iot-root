from iot.models.Type import Type
from iot.vo.sonoff import SonoffVO
from iot.mqtt import mqtt
from iot.serializer.typeSerializer import TypeSerializer
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
import jsonpickle
import time
import json


class TypeListView(ListAPIView):
    serializer_class = TypeSerializer
    queryset = Type.objects.filter(status=True)


class testApiView(APIView):
    def get(self, request, format=None):
        # Defines topic a escuchar
        mqtt.subscribeTopic = "tele/jeem/STATE"

        # Declaras la suscripcion para estar en escucha
        # SIEMPRE USAR mqtt.subscribeTopic
        mqtt.client.subscribe(mqtt.subscribeTopic)

        # Mandas a solicitar la informacion al sonoff
        mqtt.client.publish("cmnd/jeem/POWER", "TOGGLE")

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
                    mqtt.client.publish("cmnd/jeem/POWER", "TOGGLE")
                else:
                    validation = False
                    # Transformacion de JSON a VO del tipo Sonoff
                    response = SonoffVO(mqtt.globalResponse)
                    # Liberacion de variable de respuesta global
                    mqtt.globalResponse = None

        # Ejemplo de manipulacion de datos JSON recividos
        response.Sleep = "MODIFICACION 1ER NIVEL"
        response.Wifi.AP = "MODIFICACION 2DO NIVEL"

        # Validacion si presenta un error de respuesta
        if error:
            return Response({"Error": "No se encontro respuesta del dispositivo"})
        else:
            # Uso de libreria externa jsonpickle para transformar objeto VO en JSON retornarlo
            return Response(json.loads(jsonpickle.encode(response)))
