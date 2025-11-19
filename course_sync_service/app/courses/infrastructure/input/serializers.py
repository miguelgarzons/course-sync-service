from rest_framework import serializers
from collections import defaultdict
import re

class CursoSerializer(serializers.Serializer):
    fullname = serializers.CharField(max_length=255, required=True)
    shortname = serializers.CharField(max_length=255, required=True)
    categoryid = serializers.IntegerField(required=True)
    startdate = serializers.IntegerField(required=True)
    enddate = serializers.IntegerField(required=True)
    visible = serializers.IntegerField(required=True)

class MoodleQueryParamsSerializer(serializers.Serializer):
    """
    Serializer que parsea automáticamente los query params de Moodle.
    Uso: MoodleQueryParamsSerializer(data=request.query_params)
    """
    wstoken = serializers.CharField(required=True)
    wsfunction = serializers.CharField(required=True)
    moodlewsrestformat = serializers.CharField(required=True)
    courses = CursoSerializer(many=True, required=True)
    
    def to_internal_value(self, data):
        """
        Convierte automáticamente courses[0][field] a estructura anidada
        y maneja campos enteros vacíos.
        """
        parsed_data = {
            'wstoken': data.get('wstoken'),
            'wsfunction': data.get('wsfunction'),
            'moodlewsrestformat': data.get('moodlewsrestformat'),
        }
        
        cursos_dict = defaultdict(dict)
        patron = re.compile(r'courses\[(\d+)\]\[(\w+)\]')
        
        for clave, valor in data.items():
            match = patron.match(clave)
            if match:
                indice = int(match.group(1))
                campo = match.group(2)
                if campo in ['categoryid', 'startdate', 'enddate', 'visible']:
                    if valor == '':
                        raise serializers.ValidationError({campo: 'Este campo es obligatorio y debe ser un número.'})
                    try:
                        valor = int(valor)
                    except ValueError:
                        raise serializers.ValidationError({campo: f'Valor inválido: {valor}'})
                elif campo in ['fullname', 'shortname']:
                    if valor == '':
                        raise serializers.ValidationError({campo: 'Este campo es obligatorio.'})
                
                cursos_dict[indice][campo] = valor
        parsed_data['courses'] = [
            cursos_dict[i] for i in sorted(cursos_dict.keys())
        ]
        
        return super().to_internal_value(parsed_data)
