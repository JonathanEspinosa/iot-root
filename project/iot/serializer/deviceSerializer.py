from iot.models.Device import Device
from rest_framework import serializers

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ("devicecode", "groupcode", "typecode", "name", "status") 

class DeviceTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ("devicecode", "groupcode", "typecode", "name", "status")
