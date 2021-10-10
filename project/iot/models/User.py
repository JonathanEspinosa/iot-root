from django.db import models

class User(models.Model):
    usercode = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=32)
    name = models.CharField(max_length=50, default="")
    email = models.CharField(max_length=50, default="")
    phone = models.CharField(max_length=15, default="")
    status = models.BooleanField(default=False)
