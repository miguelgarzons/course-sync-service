from django.db import models


class RegistroCalificado(models.Model):
    llave_documento = models.CharField(
        "Llave del documento", max_length=300, unique=True
    )
    tipo = models.CharField("Tipo de documento", max_length=50, null=True, blank=True)

    snies = models.CharField("SNIES", max_length=50, unique=True, null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.llave_documento
