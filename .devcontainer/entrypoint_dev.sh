#!/bin/bash
set -e

echo "=== 🚀 Iniciando entorno local de desarrollo ==="

echo "⌛ Esperando a que las bases de datos estén listas..."


echo "📊 Verificando PostgreSQL..."
until python -c "import psycopg2; psycopg2.connect(host='${POSTGRES_HOST}', user='${POSTGRES_USER}', password='${POSTGRES_PASSWORD}', dbname='${POSTGRES_DB}')" &> /dev/null; do
  echo "⏳ PostgreSQL no está listo - esperando..."
  sleep 2
done
echo "✅ PostgreSQL está listo"


echo "📦 Aplicando migraciones..."
python manage.py migrate --noinput

echo "👤 Verificando superusuario y grupo admin..."
python manage.py shell << 'END'
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
import os

User = get_user_model()
username = os.getenv("DJANGO_SUPERUSER_USERNAME", "admin")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "admin")
email = os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@example.com")

# Crear o obtener el grupo "admin"
admin_group, created = Group.objects.get_or_create(name='admin')
if created:
    print(f"✅ Grupo 'admin' creado.")
else:
    print(f"ℹ️  El grupo 'admin' ya existe.")

# Crear o obtener el superusuario
if not User.objects.filter(username=username).exists():
    user = User.objects.create_superuser(username=username, password=password, email=email)
    print(f"✅ Superusuario '{username}' creado.")
else:
    user = User.objects.get(username=username)
    print(f"ℹ️  El superusuario '{username}' ya existe.")

# Agregar el usuario al grupo admin
if not user.groups.filter(name='admin').exists():
    user.groups.add(admin_group)
    print(f"✅ Usuario '{username}' agregado al grupo 'admin'.")
else:
    print(f"ℹ️  El usuario '{username}' ya pertenece al grupo 'admin'.")
END

echo "✅ Todo listo. Iniciando servidor de desarrollo..."
exec "$@"