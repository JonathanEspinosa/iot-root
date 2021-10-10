from iot.models.RolDevice import RolDevice
from rest_framework import serializers


class RolDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolDevice
        fields = ("rolcode", "devicecode", "status")
