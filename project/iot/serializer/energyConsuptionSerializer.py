from iot.models.EnergyConsuption import EnergyConsuption
from rest_framework import serializers

class EnergyConsuptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnergyConsuption
        fields = ("eneconcode", "groupcode", "date", "energyday") 
