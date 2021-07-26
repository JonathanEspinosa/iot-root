from django.db import models


class Type(models.Model):
    typecode = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    status = models.BooleanField(default=False)

class Meta(object):
    app_label = "models"