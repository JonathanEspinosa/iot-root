from typing import List
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.generic.base import View
from django.views import View
from iot.models import RolDevice
from iot.serializer.rolDeviceSerializer import RolDeviceSerializer
from rest_framework.generics import ListAPIView
# Crear la vista 
class  List_RolDevice(ListAPIView):
    serializer_class = RolDeviceSerializer
    permission_classes = ()
    def get(self, request, rolcode):
        roldevices = list(RolDevice.objects.filter(rolcode=rolcode).values())
        if len(roldevices)>0:
            datos={'message': "Success", 'roldevice':roldevices}
        else: 
            datos={'message': "Success not found..."}  
        return JsonResponse(datos)