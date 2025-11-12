from rest_framework import serializers
from app.Core.infrastructure.models import RegistroCalificado


def validar_llave_maestra(value):
    """
    Valida que la llave maestra:
    - No sea nula ni vacía.
    - Exista en RegistroCalificado.
    Devuelve la instancia de RegistroCalificado correspondiente.
    """
    # Validar null
    if value is None:
        raise serializers.ValidationError(
            "El campo 'llave_maestra' es obligatorio y no puede ser nulo."
        )

    # Validar vacío o espacios
    if isinstance(value, str) and not value.strip():
        raise serializers.ValidationError(
            "El campo 'llave_maestra' no puede estar vacío."
        )

    # Intentar obtener la instancia del modelo
    try:
        registro = RegistroCalificado.objects.get(llave_documento=value)
    except RegistroCalificado.DoesNotExist:
        raise serializers.ValidationError(
            f"La llave maestra '{value}' no existe en RegistroCalificado."
        )

    # Devolver la instancia encontrada (para asignar al ForeignKey)
    return registro
