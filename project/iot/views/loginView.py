from typing import List
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.generic.base import View
from django.views import View
from iot.models import User
# Crear la vista 
class  Login(View):

    def get(self, request, username='', password=''):
        users = list(User.objects.filter(username=username,password=password).values())
        if len(users)>0:
            datos={'message': "Success", 'users':users}
        else: 
            datos={'message': "Success not found..."}  
        return JsonResponse(datos)