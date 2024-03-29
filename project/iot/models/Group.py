from django.db import models


class Group(models.Model):
    groupcode = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    status = models.BooleanField(default=False)
    fathercode = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE
    )


class Meta(object):
    app_label = "models"
