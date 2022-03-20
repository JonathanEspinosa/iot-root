import json
from typing import List
import jsonpickle
from rest_framework.response import Response
from iot.vo.genericResponse import GenericResponse
from rest_framework.views import APIView
from iot.vo.device import DeviceVO
from django.db.models.aggregates import Max
from django.http.response import JsonResponse
from rest_framework import status
from iot.models.Device import Device
from iot.serializer.deviceSerializer import DeviceTableSerializer, DeviceSerializer
from rest_framework.generics import ListAPIView
from iot.vo.deviceSelect import DeviceSelectVO


class Create(APIView):
    def post(self, request, format=None):
        deviceVo = DeviceVO(json.dumps(request.data))
        valObj = Device.objects.filter(name=deviceVo.name).first()
        response = GenericResponse()
        if valObj != None:
            repeatedName = getattr(valObj, "name")
            response.error = 1
            response.message = (
                "Ya existe un dispositivo registrado con el nombre '"
                + repeatedName
                + "' por favor cambielo"
            )
            return JsonResponse(
                json.loads(jsonpickle.encode(response)), status=status.HTTP_201_CREATED
            )
        else:
            deviceVo.devicecode = (
                0
                if Device.objects.aggregate(Max("devicecode"))["devicecode__max"] is None
                else Device.objects.aggregate(Max("devicecode"))["devicecode__max"]
            ) + 1
            deviceVo.status = True
            device_serializer = DeviceSerializer(
                data=json.loads(jsonpickle.encode(deviceVo))
            )
            if device_serializer.is_valid():
                device_serializer.save()
                response = GenericResponse()
                response.error = 0
                response.message = ""
                return JsonResponse(
                    json.loads(jsonpickle.encode(response)),
                    status=status.HTTP_201_CREATED,
                )
            return JsonResponse(
                device_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class Update(APIView):
    def post(self, request, format=None):
        deviceVo = DeviceVO(request.body)
        valObj = (
            Device.objects.filter(name=deviceVo.name)
            .exclude(devicecode=deviceVo.devicecode)
            .first()
        )
        response = GenericResponse()
        if valObj != None:
            repeatedName = getattr(valObj, "name")
            response.error = 1
            response.message = (
                "Ya existe un dispositivo registrado con el nombre '"
                + repeatedName
                + "' por favor cambielo"
            )
            return JsonResponse(
                json.loads(jsonpickle.encode(response)), status=status.HTTP_201_CREATED
            )
        else:
            retrieveObj = Device.objects.get(devicecode=deviceVo.devicecode)
            device_serializer = DeviceSerializer(
                retrieveObj, data=json.loads(jsonpickle.encode(deviceVo))
            )
            if device_serializer.is_valid():
                device_serializer.save()
                response.error = 0
                return JsonResponse(
                    json.loads(jsonpickle.encode(response)),
                    status=status.HTTP_201_CREATED,
                )
            return JsonResponse(
                device_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


# Lista los dispositivos buscados por padre para front
class FilterTableByGroupCode(ListAPIView):
    serializer_class = DeviceTableSerializer
    permission_classes = ()

    def get_queryset(self):
        return Device.objects.filter(groupcode=self.kwargs.get("groupcode"))

# Listar todos los dispositivos para asignar en roles


class ListAll(APIView):
    def get(self, request, format=None):
        responseList: List[DeviceSelectVO] = []
        for device in Device.objects.filter(status=True).exclude(typecode=3):
            resp = DeviceSelectVO()
            group = getattr(device, "groupcode")
            resp.devicecode = getattr(device, "devicecode")
            resp.name = getattr(device, "name")
            resp.groupname = getattr(group, "name")
            resp.status = getattr(device, "status")
            responseList.append(resp)
        return Response(json.loads(jsonpickle.encode(responseList)))
