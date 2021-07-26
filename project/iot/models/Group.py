from django.db import models


class Group(models.Model):
    groupcode = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=10)
    status = models.BooleanField(default=False)

class Meta(object):
    app_label = "models"