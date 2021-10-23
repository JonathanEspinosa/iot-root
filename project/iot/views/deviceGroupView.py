from typing import List
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.generic.base import View
from django.views import View
from iot.models import Device
from iot.serializer.deviceSerializer import DeviceSerializer
from rest_framework.generics import ListAPIView

# Crear la vista 
class  List_GroupDevice(ListAPIView):

    serializer_class = DeviceSerializer
    permission_classes = ()
    def get(self, request, devicecode):
        devices = list(Device.objects.filter(devicecode=devicecode).values())
        if len(devices)>0:
            datos={'message': "Success", 'devices':devices}
        else: 
            datos={'message': "Success not found..."}  
        return JsonResponse(datos)