#!/bin/bash
set -e

echo "Iniciando aplicacion SoftBee..."

echo "Esperando a que PostgreSQL este listo..."
while ! pg_isready -h db -p 5432 -U ${PGUSER:-postgres} > /dev/null 2>&1; do
    sleep 1
done
echo "PostgreSQL esta listo!"

echo "Ejecutando migraciones de base de datos..."
flask db upgrade || echo "No se pudieron ejecutar las migraciones"

echo "Iniciando servidor Gunicorn..."
exec gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 --access-logfile - --error-logfile - index:app
