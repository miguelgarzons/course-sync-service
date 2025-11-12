
from rest_framework import serializers
from app.shared.validators.validators import validar_llave_maestra

class LlaveMaestraField(serializers.CharField):
    def to_internal_value(self, data):
        return validar_llave_maestra(data)
