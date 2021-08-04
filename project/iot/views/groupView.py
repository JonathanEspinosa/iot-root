from iot.mqtt.mqtt import client
from iot.models.Group import Group
from iot.serializer.groupSerializer import GroupSerializer
from rest_framework.generics import ListAPIView


class GroupListView(ListAPIView):
    serializer_class = GroupSerializer
    permission_classes = ()
    queryset = Group.objects.all()
