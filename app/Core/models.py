# app/models.py
import os
from .infrastructure.models import *
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

# Storage dentro del repo: app/Core/data
# base_url hace que obj.archivo.url devuelva /media/plantillas/...
plantillas_storage = FileSystemStorage(
    location=os.path.join(settings.BASE_DIR, "app", "Core", "data"),
    base_url="/media/plantillas/",
)


def plantilla_repo_path(instance, filename):
    # Guarda en: app/Core/data/<tipo>/<filename>
    return os.path.join(instance.tipo, filename)


class PlantillaDocumento(models.Model):
    TIPO_CHOICES = [
        ("Nuevo", "Nuevo"),
        ("Renovación", "Renovación"),
        ("Modificación", "Modificación"),
    ]

    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    archivo = models.FileField(
        storage=plantillas_storage, upload_to=plantilla_repo_path
    )
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"


# Elimina el archivo del disco cuando se borra el registro
@receiver(post_delete, sender=PlantillaDocumento)
def eliminar_archivo_plantilla(sender, instance, **kwargs):
    if instance.archivo and instance.archivo.storage.exists(instance.archivo.name):
        instance.archivo.delete(save=False)
