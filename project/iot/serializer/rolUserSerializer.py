from iot.models.RolUser import RolUser
from rest_framework import serializers


class RolUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolUser
        fields = ("rolcode", "usercode", "status")
