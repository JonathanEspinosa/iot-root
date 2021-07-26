from iot.models.User import User
from iot.models import Rol
from django.db import models


class RolUser(models.Model):
    rolcode = models.ForeignKey(Rol, null=False, blank=False, on_delete=models.CASCADE)
    usercode = models.ForeignKey(
        User, null=False, blank=False, on_delete=models.CASCADE
    )
    status = models.BooleanField(default=False)
