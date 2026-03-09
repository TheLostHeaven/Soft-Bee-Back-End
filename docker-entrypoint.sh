#!/bin/bash
set -e

echo "🚀 Iniciando aplicación SoftBee..."

# Esperar a que la base de datos esté lista
echo "⏳ Esperando a que PostgreSQL esté listo..."
while ! pg_isready -h db -p 5432 -U ${PGUSER:-postgres} > /dev/null 2>&1; do
    sleep 1
done
echo "✅ PostgreSQL está listo!"

# Ejecutar migraciones
echo "🔄 Ejecutando migraciones de base de datos..."
flask db upgrade || echo "⚠️  No se pudieron ejecutar las migraciones (puede ser normal en la primera ejecución)"

# Iniciar la aplicación
echo "🎉 Iniciando servidor Gunicorn..."
exec gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 --access-logfile - --error-logfile - index:app
