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


def my_cron_job():
    print("======================== TAREA PROGRAMADA =======================")
    print("=======================" +
          datetime.now().strftime("%H:%M:%S") + "========================")
    errorResponse = []
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
        if not error:
            # Empieza proceso de registro de consumo del dia de ayer
            yesterday = date.today() - timedelta(days=1)
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
                "No se encontro respuesta del dispositivo " + name)
            print("No se encontro respuesta del dispositivo " + name)

    print("Finalizo registro por dia")
