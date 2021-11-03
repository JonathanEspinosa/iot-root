from django.db import models


class Rol(models.Model):
    rolcode = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, default="")
    description = models.CharField(max_length=250, default="")
    status = models.BooleanField(default=False)
