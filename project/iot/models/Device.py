from iot.models.Type import Type
from iot.models.Group import Group
from django.db import models


class Device(models.Model):
    devicecode = models.IntegerField(primary_key=True)
    groupcode = models.ForeignKey(
        Group, null=False, blank=False, on_delete=models.CASCADE
    )
    typecode = models.ForeignKey(
        Type, null=False, blank=False, on_delete=models.CASCADE
    )
    name = models.CharField(max_length=20)
    status = models.BooleanField(default=False)
