from django.db import models

class Rol(models.Model):
    rolcode=models.IntegerField( primary_key=True)
    name = models.CharField(max_length=20)
    status = models.BooleanField(default=False) 
