from rest_framework import serializers
from django.contrib.auth import get_user_model

class GenerarDocumentoSerializer(serializers.Serializer):
    snies = serializers.CharField(max_length=255)

class EmailTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        """
        Validar que el usuario con este email exista.
        """
  
        User = get_user_model()

        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Usuario no encontrado con este email.")
        return value
    
class RegistroCalificadoEntitySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    llave_documento = serializers.CharField()
    tipo = serializers.CharField(allow_null=True)
    snies = serializers.CharField(allow_null=True)
    creado_en = serializers.DateTimeField()
    actualizado_en = serializers.DateTimeField()