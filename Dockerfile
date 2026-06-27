# Usar imagen base de Python
FROM python:3.11-slim

# Establecer variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Crear directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    dos2unix \
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

# Dar permisos al script de entrada (ya copiado con COPY . .)
RUN dos2unix /app/docker-entrypoint.sh && chmod +x /app/docker-entrypoint.sh

# Exponer el puerto
EXPOSE 5000

# Usar el script de entrada
ENTRYPOINT ["/app/docker-entrypoint.sh"]
