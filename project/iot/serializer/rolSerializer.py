from iot.models.Rol import Rol
from rest_framework import serializers


class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ("rolcode", "name", "description", "status")
