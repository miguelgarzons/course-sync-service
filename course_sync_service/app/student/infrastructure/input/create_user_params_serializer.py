from rest_framework import serializers
from collections import defaultdict
import re


class UserPreferenceSerializer(serializers.Serializer):
    type = serializers.CharField(required=True)
    value = serializers.CharField(required=True, allow_blank=True)


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    firstname = serializers.CharField(required=True)
    lastname = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    auth = serializers.CharField(required=True)
    preferences = UserPreferenceSerializer(many=True, required=False)


class MoodleCreateUsersSerializer(serializers.Serializer):
    """
    Serializer que parsea automáticamente los query params del endpoint:
    core_user_create_users
    """
    wstoken = serializers.CharField(required=True)
    wsfunction = serializers.CharField(required=True)
    moodlewsrestformat = serializers.CharField(required=True)
    users = UserSerializer(many=True, required=True)

    def to_internal_value(self, data):
        parsed_data = {}

        # Validación de los campos principales
        for field in ['wstoken', 'wsfunction', 'moodlewsrestformat']:
            if field not in data:
                raise serializers.ValidationError({field: 'Este parámetro es obligatorio.'})
            if data.get(field) == '':
                raise serializers.ValidationError({field: 'No puede estar vacío.'})
            parsed_data[field] = data.get(field)

        # Procesar users
        users_dict = defaultdict(lambda: defaultdict(dict))
        pref_dict = defaultdict(lambda: defaultdict(dict))

        patron_user = re.compile(r'users\[(\d+)\]\[(\w+)\]')
        patron_pref = re.compile(r'users\[(\d+)\]\[preferences\]\[(\d+)\]\[(\w+)\]')

        campos_obligatorios = [
            'username', 'password', 'firstname', 'lastname', 'email', 'auth'
        ]
        encontrados = defaultdict(set)

        for clave, valor in data.items():
            # Preferences
            m_pref = patron_pref.match(clave)
            if m_pref:
                idx_user = int(m_pref.group(1))
                idx_pref = int(m_pref.group(2))
                field_pref = m_pref.group(3)

                pref_dict[idx_user][idx_pref][field_pref] = valor
                continue

            # Campos directos de users
            m_user = patron_user.match(clave)
            if m_user:
                idx_user = int(m_user.group(1))
                field_user = m_user.group(2)

                encontrados[idx_user].add(field_user)
                users_dict[idx_user][field_user] = valor

        # Validar que haya al menos un usuario
        if not users_dict:
            raise serializers.ValidationError({
                'users': 'Debe enviar al menos un usuario con sus campos obligatorios.',
                'estructura_requerida': {
                    'users[0][username]': 'Usuario',
                    'users[0][password]': 'Contraseña',
                    'users[0][firstname]': 'Nombre',
                    'users[0][lastname]': 'Apellidos',
                    'users[0][email]': 'Correo',
                    'users[0][auth]': 'Método de autenticación',
                }
            })

        # Validar campos obligatorios
        for idx in users_dict:
            faltantes = [campo for campo in campos_obligatorios if campo not in encontrados[idx]]
            if faltantes:
                raise serializers.ValidationError({
                    'error': f'El usuario en índice {idx} tiene campos faltantes.',
                    'campos_faltantes': faltantes
                })

        # Convertir a la estructura final
        final_users = []
        for idx in sorted(users_dict.keys()):
            user_data = users_dict[idx]

            # Agregar preferences si existen
            prefs = []
            if idx in pref_dict:
                for p_idx in sorted(pref_dict[idx].keys()):
                    prefs.append(pref_dict[idx][p_idx])
                user_data['preferences'] = prefs

            final_users.append(user_data)

        parsed_data['users'] = final_users
        return super().to_internal_value(parsed_data)
