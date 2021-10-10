import json
from iot.vo.group import GroupVO
from iot.mqtt.mqtt import client
from iot.models.Group import Group
from iot.serializer.groupSerializer import GroupSerializer, GroupTableSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django.http.response import JsonResponse
from rest_framework.views import APIView
import jsonpickle
from django.db.models import Max
from rest_framework import status
from iot.vo.genericResponse import GenericResponse


class Create(APIView):
    def post(self, request, format=None):
        groupVo = GroupVO(json.dumps(request.data))
        groupVo.groupcode = (
            0
            if Group.objects.aggregate(Max("groupcode"))["groupcode__max"] is None
            else Group.objects.aggregate(Max("groupcode"))["groupcode__max"]
        ) + 1
        groupVo.status = True
        group_serializer = GroupSerializer(data=json.loads(jsonpickle.encode(groupVo)))
        if group_serializer.is_valid():
            group_serializer.save()
            return JsonResponse(group_serializer.data, status=status.HTTP_201_CREATED)

        return JsonResponse(group_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Update(APIView):
    def post(self, request, format=None):
        groupVo = GroupVO(json.dumps(request.data))
        retrieveObj = Group.objects.get(groupcode=groupVo.groupcode)
        group_serializer = GroupSerializer(
            retrieveObj, data=json.loads(jsonpickle.encode(groupVo))
        )
        if group_serializer.is_valid():
            group_serializer.save()
            response = GenericResponse()
            response.error = 0
            return JsonResponse(
                json.loads(jsonpickle.encode(response)),
                status=status.HTTP_201_CREATED,
            )
        return JsonResponse(group_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupListView(ListAPIView):
    serializer_class = GroupSerializer
    permission_classes = ()
    queryset = Group.objects.all()


# Lista los grupos principales para front, los que no poseen padre
class FindTableByCode(RetrieveAPIView):
    serializer_class = GroupTableSerializer
    permission_classes = ()
    queryset = Group.objects.all()
    lookup_field = "groupcode"


# Lista los grupos buscados por padre para front
class FilterTableByFather(ListAPIView):
    serializer_class = GroupTableSerializer
    permission_classes = ()

    def get_queryset(self):
        if int(self.kwargs.get("fathercode")) == 0:
            return Group.objects.filter(fathercode=None)
        else:
            return Group.objects.filter(fathercode=self.kwargs.get("fathercode"))
