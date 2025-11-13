from rest_framework import serializers


class VariablesSerializer(serializers.Serializer):
    proceso = serializers.CharField()
    busqueda_snies = serializers.IntegerField()
    nivel = serializers.CharField()
    ciclo = serializers.CharField()
    nombre_de_programa = serializers.CharField()
    tipo_registro = serializers.CharField()
    modalidad_programa = serializers.CharField()
    regional_programa = serializers.CharField()
    título_especialista = serializers.CharField()
    perfil_especialista = serializers.CharField()
    duracion_programa = serializers.IntegerField()
    periodicidad_programa = serializers.CharField()
    admitidos_programa = serializers.IntegerField()
    viabilidad_financiera = serializers.BooleanField()
    fecha = serializers.DateField()
    escuela_datos = serializers.CharField()
    correo_director = serializers.EmailField()
    campo_amplio = serializers.CharField()
    campo_especifico = serializers.CharField()
    campo_detallado = serializers.CharField()
    área_de_conocimiento = serializers.CharField()
    nucleo_basico = serializers.CharField()
    programas_similares = serializers.ListField(
        child=serializers.CharField()
    )


class EtiquetasDinamicasSerializer(serializers.Serializer):
    variables = VariablesSerializer()


class ActaPayloadSerializer(serializers.Serializer):
    etiquetas_dinamicas = EtiquetasDinamicasSerializer()


# ---------------------------------
# RESPUESTAS
# ---------------------------------

class ActaCreateResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    data = ActaPayloadSerializer()


class ActaRetrieveResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    data = ActaPayloadSerializer()


class ErrorResponseSerializer(serializers.Serializer):
    error = serializers.CharField()
