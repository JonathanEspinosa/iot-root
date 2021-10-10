from iot.models.User import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "usercode",
            "username",
            "password",
            "name",
            "email",
            "phone",
            "status",
        )
