from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from app.Core.infrastructure.models import RegistroCalificado
from .models import PlantillaDocumento

admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Información personal'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permisos'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Fechas importantes'), {'fields': ('last_login', 'date_joined')}),
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

@admin.register(PlantillaDocumento)
class PlantillaDocumentoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "tipo", "ver_archivo", "actualizado_en")
    list_filter = ("tipo",)
    search_fields = ("nombre",)

    def ver_archivo(self, obj):
        if obj.archivo:
            return format_html(
                '<a href="{}" target="_blank" rel="noopener noreferrer">📄 Abrir documento</a>',
                obj.archivo.url,
            )
        return "Sin archivo"

    ver_archivo.short_description = "Archivo"


@admin.register(RegistroCalificado)
class RegistroCalificadoAdmin(admin.ModelAdmin):
    list_display = ("llave_documento", "tipo", "snies", "creado_en", "actualizado_en")
    search_fields = ("llave_documento", "tipo", "snies")
    list_filter = ("tipo",)
    ordering = ("-creado_en",)
