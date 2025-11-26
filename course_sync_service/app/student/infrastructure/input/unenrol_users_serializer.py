from rest_framework import serializers
from collections import defaultdict
import re

class EnrolmentSerializer(serializers.Serializer):
    """
    Serializador de un solo enrolment/unenrolment.
    roleid es opcional porque Moodle no lo usa en unenrol_manual_unenrol_users.
    """
    userid = serializers.IntegerField(required=True)
    courseid = serializers.IntegerField(required=True)
    roleid = serializers.IntegerField(required=False)  # opcional para unenrol


class MoodleUnenrolmentParamsSerializer(serializers.Serializer):
    """
    Parser automático para parámetros Moodle como:

    enrolments[0][userid]=111
    enrolments[0][courseid]=222
    enrolments[0][roleid]=5   ← solo en enrol

    Soporta:
    - enrol_manual_enrol_users
    - enrol_manual_unenrol_users
    """
    wstoken = serializers.CharField(required=True)
    wsfunction = serializers.CharField(required=True)
    moodlewsrestformat = serializers.CharField(required=False)
    enrolments = EnrolmentSerializer(many=True, required=True)

    def to_internal_value(self, data):

        parsed_data = {
            'wstoken': data.get('wstoken'),
            'wsfunction': data.get('wsfunction'),
            'moodlewsrestformat': data.get('moodlewsrestformat', 'json'),
        }

        enrolments_dict = defaultdict(dict)

        patron = re.compile(r'enrolments\[(\d+)\]\[(\w+)\]')

        for clave, valor in data.items():
            match = patron.match(clave)
            if match:
                index = int(match.group(1))
                field = match.group(2)

                # Validación de campos numéricos
                if field in ['userid', 'courseid', 'roleid']:
                    if valor in ('', None):
                        raise serializers.ValidationError({
                            field: "Este campo es obligatorio y debe ser un número."
                        })
                    try:
                        valor = int(valor)
                    except ValueError:
                        raise serializers.ValidationError({
                            field: f"Valor inválido: {valor}. Debe ser un número."
                        })

                enrolments_dict[index][field] = valor

        # Convertir a lista ordenada
        parsed_data['enrolments'] = [
            enrolments_dict[i] for i in sorted(enrolments_dict.keys())
        ]

        return super().to_internal_value(parsed_data)
