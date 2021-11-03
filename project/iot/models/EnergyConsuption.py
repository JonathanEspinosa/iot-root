from iot.models.Group import Group
from django.db import models


class EnergyConsuption(models.Model):
    eneconcode = models.IntegerField(primary_key=True)
    groupcode = models.ForeignKey(
        Group, null=False, blank=False, on_delete=models.CASCADE
    )
    date = models.DateField(auto_now=False)
    energyday = models.FloatField(default=False) 
