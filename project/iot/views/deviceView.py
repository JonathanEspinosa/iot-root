from iot.models.Device import Device
from iot.serializer.deviceSerializer import DeviceSerializer
from rest_framework.generics import ListAPIView


class DeviceListView(ListAPIView):
    serializer_class = DeviceSerializer
    permission_classes = ()
    queryset = Device.objects.all()
