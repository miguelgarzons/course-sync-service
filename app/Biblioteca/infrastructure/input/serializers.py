from rest_framework import serializers
from django.core.validators import validate_email
from datetime import datetime

from app.shared.validators.fields import LlaveMaestraField


class EtiquetasDinamicasSerializer(serializers.Serializer):
    etiquetas_dinamicas = serializers.DictField()
    llave_maestra = LlaveMaestraField()

    def validate(self, data):
        etiquetas = data.get("etiquetas_dinamicas", {})
        if "variables" not in etiquetas:
            raise serializers.ValidationError({"etiquetas_dinamicas": "Debe contener la clave 'variables'."})

        variables = etiquetas.get("variables", {})
        if not isinstance(variables, dict):
            raise serializers.ValidationError({"variables": "El valor de 'variables' debe ser un objeto (dict)."})

        errores = {}
        for nombre, valor in variables.items():
            error = self._validar_variable(nombre, valor)
            if error:
                errores[nombre] = error

        if errores:
            raise serializers.ValidationError({"variables": errores})

        return data

    def _validar_variable(self, nombre, valor):
        """
        Reglas dinámicas de validación según el tipo de dato detectado.
        """
        if valor is None or valor == "":
            return "El campo no puede estar vacío."

        if nombre == "correo_director":
            try:
                validate_email(valor)
            except Exception:
                return "Debe ser un correo electrónico válido."

        if nombre == "fecha":
            try:
                datetime.strptime(valor, "%Y-%m-%d")
            except Exception:
                return "La fecha debe tener el formato YYYY-MM-DD."

        if nombre == "viabilidad_financiera" and not isinstance(valor, bool):
            return "El campo 'viabilidad_financiera' debe ser verdadero o falso (booleano)."

        if nombre in ["busqueda_snies", "duracion_programa", "admitidos_programa"]:
            if not isinstance(valor, int):
                return "Debe ser un número entero."

        if nombre == "programas_similares":
            if not isinstance(valor, list):
                return "Debe ser una lista de valores (array)."
            if not all(isinstance(v, str) for v in valor):
                return "Cada elemento debe ser texto (string)."

        if isinstance(valor, str) and len(valor.strip()) == 0:
            return "El valor no puede estar vacío o solo contener espacios."

        return None


class BibliotecaQuerySerializer(serializers.Serializer):
    llave_id = serializers.CharField(
        required=True,
        help_text="ID del llave_id que se desea obtener"
    )

