from iot.mqtt.mqtt import client
from iot.models.Type import Type
from rest_framework import serializers


class TypeSerializer(serializers.ModelSerializer):
    newdata = serializers.SerializerMethodField()

    class Meta:
        model = Type
        fields = ("typecode", "name", "description", "status","newdata",)

    def get_newdata(self, obj):
        return 5
