

from django.db import models

# Create your models here.

class GROUP(models.Model):
    groupcode = models.IntegerField(max_length=10, primary_key=True)
    name = models.CharField(max_length=10)
    status = models.BooleanField(default=False)
class ENERGYCONSUPTION(models.Model):
    eneconcode = models.IntegerField(max_length=10, primary_key=True)
    groupcode = models.ForeignKey(GROUP, null=False, blank=False, on_delete=models.CASCADE)
    date = models.DateField(auto_now=False,name="Date Field")
    energytoday= models.IntegerField(max_length=10)
    energyyesterday= models.IntegerField(max_length=10)

class TYPE(models.Model):
    typecode=models.IntegerField(max_length=10, primary_key=True)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    status = models.BooleanField(default=False)

class DEVICE(models.Model):
    devicecode=models.IntegerField(max_length=10, primary_key=True)
    groupcode=models.ForeignKey(GROUP, null=False, blank=False, on_delete=models.CASCADE) 
    typecode=models.ForeignKey(TYPE, null=False, blank=False, on_delete=models.CASCADE) 
    topic = models.CharField(max_length=20)
    status = models.BooleanField(default=False)
class ROL(models.Model):
    rolcode=models.IntegerField(max_length=10, primary_key=True)
    name = models.CharField(max_length=20)
    status = models.BooleanField(default=False)

class ROLDEVICE(models.Model):
    rolcode = models.ForeignKey(ROL, null=False, blank=False, on_delete=models.CASCADE) 
    devicecode = models.ForeignKey(GROUP, null=False, blank=False, on_delete=models.CASCADE) 
    status = models.BooleanField(default=False)
    
class USER(models.Model):
    usercode=models.IntegerField(max_length=10, primary_key=True)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=32)
    status = models.BooleanField(default=False)
class ROLUSER(models.Model):
    rolcode = models.ForeignKey(ROL, null=False, blank=False, on_delete=models.CASCADE) 
    usercode = models.ForeignKey(USER, null=False, blank=False, on_delete=models.CASCADE) 
    status = models.BooleanField(default=False)