

from _typeshed import Self
from django.db import models
from django.db.models.query_utils import select_related_descend

# Create your models here.
class Persona(models.Model):
    idpersona=models.CharField(max_length=3, primary_key=True)
    nombre = models.CharField(max_length=10)
    apellido = models.CharField(max_length=10)
   
class Salas(models.Model):
    idsala=models.CharField(max_length=3, primary_key=True)
    nombre = models.CharField(max_length=10)
    persona = models.ForeignKey(Persona, null=False, blank=False, on_delete=models.CASCADE) 

    def _str_(Self):
        txt = "{0} ({1}) / Docente: {2}"
        return txt.format(Self.idsala, Self.nombre, Self.persona)


