from rest_framework import serializers
import re
from collections import defaultdict


class MoodleGetParamsSerializer(serializers.Serializer):
    wstoken = serializers.CharField(required=True)
    wsfunction = serializers.CharField(required=True)
    options = serializers.DictField(child=serializers.ListSerializer(
        child=serializers.IntegerField(), required=True
    ), required=True)

    def to_internal_value(self, data):
        """
        Convierte options[ids][0] y similares a una estructura Python.
        - Todos los parámetros options[*][*] deben existir.
        - Solo options[ids][0] puede venir vacío pero debe venir en la query.
        """

        # Validación de que los campos principales existan
        if 'wstoken' not in data or data.get('wstoken') in (None, ''):
            raise serializers.ValidationError({'wstoken': 'Este campo es obligatorio.'})

        if 'wsfunction' not in data or data.get('wsfunction') in (None, ''):
            raise serializers.ValidationError({'wsfunction': 'Este campo es obligatorio.'})

        parsed_data = {
            'wstoken': data.get('wstoken'),
            'wsfunction': data.get('wsfunction'),
            'options': {}
        }

        options_dict = defaultdict(list)
        patron = re.compile(r'options\[(\w+)\]\[(\d+)\]')

        # Recolectar claves para asegurar que existan
        found_keys = set()

        for clave, valor in data.items():
            match = patron.match(clave)
            if match:
                key = match.group(1)
                index = int(match.group(2))
                found_keys.add(key)

                # Validar valores vacíos
                if valor == '':
                    if not (key == 'ids' and index == 0):
                        raise serializers.ValidationError({clave: 'Este parámetro es obligatorio y no puede estar vacío.'})

                    # Se permite vacío solo en ids[0], pero debe venir en la query
                    while len(options_dict[key]) <= index:
                        options_dict[key].append(None)
                    continue

                # Convertir a entero
                try:
                    valor = int(valor)
                except ValueError:
                    raise serializers.ValidationError({clave: f'Valor inválido: {valor}'})

                while len(options_dict[key]) <= index:
                    options_dict[key].append(None)

                options_dict[key][index] = valor

        # Verificar que ids exista siempre
        if 'ids' not in found_keys:
            raise serializers.ValidationError({'options': 'Debe incluirse options[ids][0] al menos.'})

        # Limpiar None
        for key, lista in options_dict.items():
            parsed_data['options'][key] = [x for x in lista if x is not None]

        return super().to_internal_value(parsed_data)
