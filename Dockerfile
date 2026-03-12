# Usar imagen base de Python
FROM python:3.11-slim

# Establecer variables de entorno para optimización
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PORT=5000

# Crear directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de requirements
COPY requirements/base.txt requirements/base.txt
COPY requirements/production.txt requirements/production.txt

# Instalar dependencias de Python
RUN pip install --upgrade pip && \
    pip install -r requirements/production.txt

# Copiar el código de la aplicación
COPY . .

# Crear directorio para logs
RUN mkdir -p logs

# Exponer el puerto (Railway usa la variable PORT)
EXPOSE ${PORT}

# Comando optimizado para Railway con menos workers (reduce consumo de RAM)
CMD gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 2 --worker-class gthread --timeout 120 --max-requests 1000 --max-requests-jitter 50 --access-logfile - --error-logfile - index:app
