#!/bin/bash
set -e

echo "=== 🚀 Iniciando entrypoint (entorno:) ==="

echo "⌛ Esperando a que la base de datos esté disponible..."
sleep 5



echo "✅ Entrypoint completado. Iniciando aplicación..."
exec "$@"
