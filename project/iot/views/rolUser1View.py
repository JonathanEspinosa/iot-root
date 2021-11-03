from typing import List
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.generic.base import View
from django.views import View
from iot.models import RolUser
from iot.serializer.rolUserSerializer import RolUserSerializer
from rest_framework.generics import ListAPIView

# Crear la vista 
class  List_Rol(ListAPIView):

    serializer_class = RolUserSerializer
    permission_classes = ()
    def get(self, request, usercode):
        rolusers = list(RolUser.objects.filter(usercode=usercode).values())
        if len(rolusers)>0:
            datos={'message': "Success", 'RolUser':rolusers}
        else: 
            datos={'message': "Success not found..."}  
        return JsonResponse(datos)
       

