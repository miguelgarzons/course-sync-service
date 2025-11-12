from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget
from .models import Acta


@admin.register(Acta)
class ActaAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }

    list_display = ("llave_maestra", "creado_por", "modificado_por", "creado_en", "actualizado_en")
    search_fields = ("llave_maestra__llave_documento", "creado_por__email")
    readonly_fields = ("creado_en", "actualizado_en", "creado_por", "modificado_por")

    fieldsets = (
        (
            "Información General",
            {
                "fields": ("llave_maestra",),
            },
        ),
        (
            "Etiquetas dinámicas",
            {
                "fields": ("etiquetas_dinamicas",),
                "description": "Agrega o edita etiquetas dinámicas en formato JSON (usa comillas dobles).",
            },
        ),
        (
            "Auditoría",
            {
                "fields": ("creado_por", "modificado_por", "creado_en", "actualizado_en"),
                "description": "Campos de control de auditoría, se completan automáticamente.",
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        """
        ✅ Sobrescribimos el guardado para registrar quién crea o modifica desde el admin.
        """
        if not obj.pk:
            obj.creado_por = request.user
        else:
            obj.modificado_por = request.user
        super().save_model(request, obj, form, change)
