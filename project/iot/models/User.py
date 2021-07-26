from django.db import models


class User(models.Model):
    usercode = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=32)
    status = models.BooleanField(default=False)
