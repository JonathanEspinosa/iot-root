from typing import List
from django.http.response import JsonResponse
from django.shortcuts import render
from iot.models.Group import Group
from iot.serializer.groupSerializer import GroupSerializer
from rest_framework.generics import ListAPIView


class GroupidListView(ListAPIView):
  def get(self, request, groupcode=0):
        groups = list(Group.objects.filter(groupcode=groupcode).values())
        if len(groups)>0:
            datos={'message': "Success", 'Group':groups}
        else: 
            datos={'message': "Success not found..."}  
        return JsonResponse(datos)
