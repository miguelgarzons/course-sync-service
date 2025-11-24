from rest_framework import serializers
from collections import defaultdict
import re

class CursoSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    fullname = serializers.CharField(max_length=255, required=True, allow_blank=True)
    shortname = serializers.CharField(max_length=255, required=True, allow_blank=True)
    categoryid = serializers.IntegerField(required=True, allow_null=True)
    startdate = serializers.IntegerField(required=True, allow_null=True)
    enddate = serializers.IntegerField(required=True, allow_null=True)
    visible = serializers.IntegerField(required=True, allow_null=True)

class MoodleUpdateParamsSerializer(serializers.Serializer):
    """
    Serializer que parsea automáticamente los query params de Moodle.
    Todos los campos son obligatorios pero pueden venir vacíos.
    """
    wstoken = serializers.CharField(required=True)
    wsfunction = serializers.CharField(required=True)
    moodlewsrestformat = serializers.CharField(required=True)
    courses = CursoSerializer(many=True, required=True)

    def to_internal_value(self, data):
        parsed_data = {}

        # Validación de los campos principales (obligatorios y no vacíos)
        for field in ['wstoken', 'wsfunction', 'moodlewsrestformat']:
            if field not in data:
                raise serializers.ValidationError({field: 'Este parámetro es obligatorio.'})
            if data.get(field) == '':
                raise serializers.ValidationError({field: 'No puede estar vacío.'})
            parsed_data[field] = data.get(field)

        # Procesar los courses
        cursos_dict = defaultdict(dict)
        patron = re.compile(r'courses\[(\d+)\]\[(\w+)\]')

        campos_obligatorios = [
            'id', 'fullname', 'shortname',
            'categoryid', 'startdate', 'enddate', 'visible'
        ]
        encontrados = defaultdict(set)

        for clave, valor in data.items():
            match = patron.match(clave)
            if match:
                indice = int(match.group(1))
                campo = match.group(2)

                # Registrar el campo como encontrado
                encontrados[indice].add(campo)

                # PERMITIR VALORES VACÍOS
                if campo in ['categoryid', 'startdate', 'enddate', 'visible']:
                    if valor == '':
                        cursos_dict[indice][campo] = None
                    else:
                        try:
                            cursos_dict[indice][campo] = int(valor)
                        except ValueError:
                            raise serializers.ValidationError({clave: 'Debe ser un número válido o estar vacío.'})
                else:
                    cursos_dict[indice][campo] = valor

        # VALIDAR QUE SE HAYA ENVIADO AL MENOS UN CURSO
        if not cursos_dict:
            raise serializers.ValidationError({
                'courses': 'Debe enviar al menos un curso con todos sus campos obligatorios.',
                'estructura_requerida': {
                    'courses[0][fullname]': 'Nombre completo del curso (texto, puede estar vacío)',
                    'courses[0][shortname]': 'Nombre corto del curso (texto, puede estar vacío)',
                    'courses[0][categoryid]': 'ID de categoría (número entero, puede estar vacío)',
                    'courses[0][startdate]': 'Fecha de inicio en timestamp (número entero, puede estar vacío)',
                    'courses[0][enddate]': 'Fecha de fin en timestamp (número entero, puede estar vacío)',
                    'courses[0][visible]': 'Visibilidad del curso (número entero 0 o 1, puede estar vacío)'
                },
                'ejemplo': 'courses[0][fullname]=Mi Curso&courses[0][shortname]=MC&courses[0][categoryid]=1&courses[0][startdate]=1640995200&courses[0][enddate]=1672531200&courses[0][visible]=1'
            })

        # Validar que todos los cursos tengan todos los campos obligatorios
        for indice in cursos_dict.keys():
            campos = encontrados[indice]
            faltantes = []
            for campo in campos_obligatorios:
                if campo not in campos:
                    faltantes.append(f"courses[{indice}][{campo}]")
            
            if faltantes:
                raise serializers.ValidationError({
                    'error': f'El curso en el índice {indice} tiene campos faltantes.',
                    'campos_faltantes': faltantes,
                    'campos_obligatorios': {
                        f'courses[{indice}][fullname]': 'Nombre completo del curso (texto, puede estar vacío)',
                        f'courses[{indice}][shortname]': 'Nombre corto del curso (texto, puede estar vacío)',
                        f'courses[{indice}][categoryid]': 'ID de categoría (número entero, puede estar vacío)',
                        f'courses[{indice}][startdate]': 'Fecha de inicio en timestamp (número entero, puede estar vacío)',
                        f'courses[{indice}][enddate]': 'Fecha de fin en timestamp (número entero, puede estar vacío)',
                        f'courses[{indice}][visible]': 'Visibilidad del curso (número entero 0 o 1, puede estar vacío)'
                    }
                })

        # Crear lista ordenada de cursos
        parsed_data['courses'] = [
            cursos_dict[i] for i in sorted(cursos_dict.keys())
        ]

        return super().to_internal_value(parsed_data)