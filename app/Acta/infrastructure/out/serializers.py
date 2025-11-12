from rest_framework import serializers


class ActaResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    llave_maestra = serializers.CharField()
    creado_en = serializers.DateTimeField()


class ActaDetailResponseSerializer(ActaResponseSerializer):
    actualizado_en = serializers.DateTimeField(required=False)
    creado_por_id = serializers.IntegerField(required=False)
    etiquetas_dinamicas = serializers.DictField(required=False)