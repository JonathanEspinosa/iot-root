from iot.models.Rol import Rol
from iot.models.Device import Device
from django.db import models


class RolDevice(models.Model):
    rolcode = models.ForeignKey(Rol, null=False, blank=False, on_delete=models.CASCADE)
    devicecode = models.ForeignKey(
        Device, null=False, blank=False, on_delete=models.CASCADE
    )
    status = models.BooleanField(default=False)

    class Meta:
        unique_together = (("rolcode", "devicecode"),)
