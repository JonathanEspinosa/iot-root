

from django.db import models

# Create your models here.
class Persona(models.Model):
    idpersona=models.CharField(max_length=3, primary_key=True)
    nombre = models.CharField(max_length=10)
    apellido = models.CharField(max_length=10)
    
    
    def nombreCompleto(self):
        txt = "{0} {1},{2}"
        return txt.format(self.nombre, self.apellido)
        
    def _str_(self):
       return self.nombreCompleto()


class Salas(models.Model):
    idsala=models.CharField(max_length=3, primary_key=True)
    nombre = models.CharField(max_length=10)
    persona = models.ForeignKey(Persona, null=False, blank=False, on_delete=models.CASCADE) 
    def _str_(self):
       return "{0} ({1})".format(self.nombre, self.persona)
    

