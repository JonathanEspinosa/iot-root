from typing import List
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.generic.base import View
from django.views import View
from iot.models import RolDevice
from iot.serializer.rolDeviceSerializer import RolDeviceSerializer
from rest_framework.generics import ListAPIView
# Crear la vista 
class RolDeviceAlltView(ListAPIView):
    serializer_class = RolDeviceSerializer
    permission_classes = ()
    queryset = RolDevice.objects.all()
