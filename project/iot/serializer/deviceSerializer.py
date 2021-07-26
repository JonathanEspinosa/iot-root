from iot.models.Device import Device
from rest_framework import serializers


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ("devicecode", "groupcode", "typecode", "topic", "status")

        # GROUP, null=False, blank=False, on_delete=models.CASCADE
        # TYPE, null=False, blank=False, on_delete=models.CASCADE
