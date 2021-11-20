from datetime import date, datetime, timedelta
from django.db.models.aggregates import Max, Min, Sum
from django.http.response import JsonResponse
from rest_framework.response import Response
from iot.mqtt import mqtt
from rest_framework.views import APIView
from iot.vo.energyConsuption import EnergyConsuptionVO
from iot.models.EnergyConsuption import EnergyConsuption
from iot.serializer.energyConsuptionSerializer import EnergyConsuptionSerializer
from iot.models.Device import Device
import json
import time
import jsonpickle


class CheckEnergyConsumption(APIView):
    def post(self, request, format=None):
        toJson = json.loads(json.dumps(request.data))
        minDate: date = datetime.fromisoformat(toJson["minDate"])
        maxDate: date = datetime.fromisoformat(toJson["maxDate"])
        # print(minDate)
        # print(maxDate)
        # for item in (EnergyConsuption.objects
        #              .filter(groupcode=toJson["groupcode"])
        #              .filter(date__gte=minDate)
        #              .filter(date__lte=maxDate)):
        #     print(str(getattr(item, "date")) + '==' +
        #           str(getattr(item, "energyday")))
        energy = (EnergyConsuption.objects
                  .filter(groupcode=toJson["groupcode"])
                  .filter(date__gte=minDate)
                  .filter(date__lte=maxDate)
                  .aggregate(Sum("energyday"))["energyday__sum"]
                  )
        return Response({"energy": energy})


class RangeDateByGroup(APIView):
    def get(self, request, groupcode):
        minDate: date = (EnergyConsuption.objects.filter(groupcode=groupcode)
                         .aggregate(Min("date"))["date__min"])
        maxDate: date = None
        if(minDate is None):
            minDate = date.today().ctime()
            maxDate = (date.today() - timedelta(days=1)).ctime()
        else:
            minDate = minDate.ctime()
            maxDate: date = (EnergyConsuption.objects.filter(groupcode=groupcode)
                             .aggregate(Max("date"))["date__max"])
            maxDate = maxDate.ctime()
        print('***************************************')
        print(minDate)
        print(maxDate)
        print('***************************************')
        return Response({"minDate": minDate, "maxDate": maxDate})


class RegisterDay(APIView):
    def get(self, request, format=None):
        # def my_cron_job():
        errorResponse = []
    # energyday: float sumo todos los dias para dar el resultado, no usar el total'
        for device in Device.objects.filter(typecode=3):
            name = getattr(device, "name")
            # Defines topic a escuchar
            mqtt.subscribeTopic = "stat/"+name+"/STATUS8"
            # Declaras la suscripcion para estar en escucha SIEMPRE USAR mqtt.subscribeTopic
            mqtt.client.subscribe(mqtt.subscribeTopic)
            # Mandas a solicitar la informacion al sonoff
            mqtt.client.publish("cmnd/"+name+"/Status", "8")
            # validas si la variable global tiene o no respuesta
            validation = True
            error = False
            count = 0
            energyDay: float = 0
            # Ciclo para esperar respuesta mqtt
            # 3 oportunidades de 1 seg; En cada oportunidad ejecuta la llamada de nuevo; Si en las 3 oportunidades no hay respuesta, corta proceso y manda error
            while validation:
                count += 1
                if count == 3:
                    error = True
                    validation = False

                if not error:
                    time.sleep(1)
                    if mqtt.globalResponse is None:
                        mqtt.client.publish("cmnd/"+name+"/Status", "8")
                    else:
                        validation = False
                        energyDay = json.loads(mqtt.globalResponse)[
                            "StatusSNS"]["ENERGY"]["Yesterday"]
                        print(energyDay)
                        # Liberacion de variable de respuesta global
                        mqtt.globalResponse = None
                        mqtt.client.unsubscribe(mqtt.subscribeTopic)

            # Validacion si presenta un error de respuesta
            print(error)
            if not error:
                # Empieza proceso de registro de consumo del dia de ayer
                yesterday = date.today() - timedelta(days=1)
                # yesterday = date.today() + timedelta(days=3)
                print('**********************yesterday*****************')
                print(yesterday)
                retrieveObj = (
                    EnergyConsuption.objects
                    .filter(date=yesterday)
                    .filter(groupcode=getattr(device, "groupcode"))
                    .first()
                )

                energyConsuptionVO = EnergyConsuptionVO()
                groAux = getattr(device, "groupcode")
                energyConsuptionVO.groupcode = getattr(groAux, "groupcode")
                energyConsuptionVO.date = yesterday.isoformat()
                energyConsuptionVO.energyday = energyDay
                if retrieveObj == None:
                    energyConsuptionVO.eneconcode = (0
                                                     if EnergyConsuption.objects.aggregate(Max("eneconcode"))["eneconcode__max"] is None
                                                     else EnergyConsuption.objects.aggregate(Max("eneconcode"))["eneconcode__max"]
                                                     ) + 1
                    energyConsuption_serializer = EnergyConsuptionSerializer(
                        data=json.loads(jsonpickle.encode(energyConsuptionVO)))
                    print("*****************create*****************")
                    print(jsonpickle.encode(energyConsuptionVO))
                    if energyConsuption_serializer.is_valid():
                        energyConsuption_serializer.save()
                else:
                    energyConsuptionVO.eneconcode = getattr(
                        retrieveObj, "eneconcode")
                    print("*****************update*****************")
                    print(jsonpickle.encode(energyConsuptionVO))
                    energyConsuption_serializer = EnergyConsuptionSerializer(retrieveObj,
                                                                             data=json.loads(jsonpickle.encode(energyConsuptionVO)))
                    if energyConsuption_serializer.is_valid():
                        energyConsuption_serializer.save()

            else:
                errorResponse.append(
                    "No se encontro respuesta del dispositivo "+name)
                print("No se encontro respuesta del dispositivo "+name)

        print("Finalizo registro por dia")
        return Response({"Metodo": "Finalizo registro por dia", "errorResponse": errorResponse})
