import json
from typing import List
import jsonpickle
from rest_framework.response import Response
from iot.serializer.rolDeviceSerializer import RolDeviceSerializer
from iot.serializer.rolSerializer import RolSerializer
from django.http.response import JsonResponse
from rest_framework.views import APIView
from django.db.models import Max
from rest_framework import status
from iot.models.Rol import Rol
from iot.vo.genericResponse import GenericResponse
from iot.vo.rol import RolVO
from iot.models.Device import Device
from iot.models.RolDevice import RolDevice
from iot.vo.device import DeviceVO
from iot.vo.deviceSelect import DeviceSelectVO
from iot.vo.rolDevice import RolDeviceVO
from iot.vo.rolSelect import RolSelectVO


class Create(APIView):
    def post(self, request, format=None):
        # METODO PARA ASIGNAR DISPOSITIVOS A ROLES
        def createDeviceList(rolcode: int, deviceList: List[DeviceSelectVO]):
            response = GenericResponse()
            response.error = 0
            for item in deviceList:
                device = DeviceSelectVO(json.dumps(item))
                if device.status:
                    rolDeviceVO = RolDeviceVO()
                    rolDeviceVO.devicecode = device.devicecode
                    rolDeviceVO.rolcode = rolcode
                    rolDeviceVO.status = True
                    rolDevice_serializer = RolDeviceSerializer(
                        data=json.loads(jsonpickle.encode(rolDeviceVO))
                    )
                    if rolDevice_serializer.is_valid():
                        rolDevice_serializer.save()
                    else:
                        response.error = 1
                        response.message = (
                            response.message + rolDevice_serializer.errors
                        )
            return response

        rolVO = RolVO(json.dumps(request.data))
        valObj = Rol.objects.filter(name=rolVO.name).first()
        response = GenericResponse()
        if valObj != None:
            repeatedName = getattr(valObj, "name")
            response.error = 1
            response.message = (
                "Ya existe un rol registrado con el nombre '"
                + repeatedName
                + "' por favor cambielo"
            )
            return JsonResponse(
                json.loads(jsonpickle.encode(response)), status=status.HTTP_201_CREATED
            )
        else:
            rolVO.rolcode = (
                0
                if Rol.objects.aggregate(Max("rolcode"))["rolcode__max"] is None
                else Rol.objects.aggregate(Max("rolcode"))["rolcode__max"]
            ) + 1
            rolVO.status = True
            rol_serializer = RolSerializer(data=json.loads(jsonpickle.encode(rolVO)))

            if rol_serializer.is_valid():
                rol_serializer.save()

                response = createDeviceList(
                    rol_serializer.data["rolcode"], rolVO.deviceList
                )

                return JsonResponse(
                    json.loads(jsonpickle.encode(response)),
                    status=status.HTTP_201_CREATED,
                )
            return JsonResponse(
                rol_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

class Update(APIView):
    def post(self, request, format=None):
        def updateDeviceList(rolcode: int, deviceList: List[DeviceSelectVO]):
            response = GenericResponse()
            response.error = 0
            for item in deviceList:
                device = DeviceSelectVO(json.dumps(item))
                rolDeviceCurrent = (
                    RolDevice.objects.filter(rolcode=rolcode)
                    .filter(devicecode=device.devicecode)
                    .first()
                )
                if rolDeviceCurrent is None and device.status:
                    rolDeviceVO = RolDeviceVO()
                    rolDeviceVO.devicecode = device.devicecode
                    rolDeviceVO.rolcode = rolcode
                    rolDeviceVO.status = True
                    rolDevice_serializer = RolDeviceSerializer(
                        data=json.loads(jsonpickle.encode(rolDeviceVO))
                    )
                    if rolDevice_serializer.is_valid():
                        rolDevice_serializer.save()
                    else:
                        response.error = 1
                        response.message = (
                            response.message + rolDevice_serializer.errors
                        )
                else:
                    if (
                        rolDeviceCurrent is not None
                        and getattr(rolDeviceCurrent, "status") != device.status
                    ):
                        rolDeviceVO = RolDeviceVO()
                        rolDeviceVO.devicecode = device.devicecode
                        rolDeviceVO.rolcode = rolcode
                        rolDeviceVO.status = device.status
                        rolDevice_serializer = RolDeviceSerializer(
                            rolDeviceCurrent,
                            data=json.loads(jsonpickle.encode(rolDeviceVO)),
                        )
                        if rolDevice_serializer.is_valid():
                            rolDevice_serializer.save()
                        else:
                            response.error = 1
                            response.message = (
                                response.message + rolDevice_serializer.errors
                            )
            return response

        rolVo = RolVO(request.body)
        valObj = (
            Rol.objects.filter(name=rolVo.name).exclude(rolcode=rolVo.rolcode).first()
        )
        response = GenericResponse()
        if valObj != None:
            repeatedName = getattr(valObj, "name")
            response.error = 1
            response.message = (
                "Ya existe un rol registrado con el nombre '"
                + repeatedName
                + "' por favor cambielo"
            )
            return JsonResponse(
                json.loads(jsonpickle.encode(response)), status=status.HTTP_201_CREATED
            )
        else:
            retrieveObj = Rol.objects.get(rolcode=rolVo.rolcode)
            rol_serializer = RolSerializer(
                retrieveObj, data=json.loads(jsonpickle.encode(rolVo))
            )
            if rol_serializer.is_valid():
                rol_serializer.save()
                response = updateDeviceList(
                    rol_serializer.data["rolcode"], rolVo.deviceList
                )
                return JsonResponse(
                    json.loads(jsonpickle.encode(response)),
                    status=status.HTTP_201_CREATED,
                )
            return JsonResponse(
                rol_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


# Lista todos los roles para front
class ListAll(APIView):
    def get(self, request, format=None):
        responseList: List[RolVO] = []
        for rol in Rol.objects.all():
            resp = RolVO()
            resp.rolcode = getattr(rol, "rolcode")
            resp.name = getattr(rol, "name")
            resp.description = getattr(rol, "description")
            resp.status = getattr(rol, "status")
            resp.deviceList = []
            for union in RolDevice.objects.filter(rolcode=resp.rolcode):
                devAux = getattr(union, "devicecode")
                groAux = getattr(devAux, "groupcode")
                device = DeviceSelectVO()
                device.devicecode = getattr(devAux, "devicecode")
                device.name = getattr(devAux, "name")
                device.groupname = getattr(groAux, "name")
                device.status = getattr(union, "status")
                resp.deviceList.append(device)
            responseList.append(resp)
        return Response(json.loads(jsonpickle.encode(responseList)))

        
# Listar todos los roles para asignar en usuarios        
class ListAllActive(APIView):
    def get(self, request, format=None):
        responseList: List[RolSelectVO] = []
        for rol in Rol.objects.filter(status=True):
            resp = RolSelectVO()
            resp.rolcode = getattr(rol, "rolcode")
            resp.name = getattr(rol, "name")
            resp.description = getattr(rol, "description")
            resp.status = getattr(rol, "status")
            responseList.append(resp)
        return Response(json.loads(jsonpickle.encode(responseList)))
