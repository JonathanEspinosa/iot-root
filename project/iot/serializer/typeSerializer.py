from iot.models.Type import Type
from rest_framework import serializers


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ("typecode", "name", "description", "status")
