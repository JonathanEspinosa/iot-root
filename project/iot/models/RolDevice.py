from iot.models.Rol import Rol
from iot.models.Group import Group
from django.db import models


class RolDevice(models.Model):
    rolcode = models.ForeignKey(Rol, null=False, blank=False, on_delete=models.CASCADE)
    devicecode = models.ForeignKey(
        Group, null=False, blank=False, on_delete=models.CASCADE
    )
    status = models.BooleanField(default=False)
