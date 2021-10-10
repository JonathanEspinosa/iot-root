from iot.models.Group import Group
from rest_framework import serializers

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("fathercode", "groupcode", "name", "status")

class GroupTableSerializer(serializers.ModelSerializer):
    typecode = serializers.SerializerMethodField()
    class Meta:
        model = Group
        fields = ("fathercode", "groupcode", "name", "typecode", "status")
    def get_typecode(self, obj):
        return 2
