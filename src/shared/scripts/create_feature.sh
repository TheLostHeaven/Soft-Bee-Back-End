#!/bin/bash
# scripts/create_feature.sh

FEATURE_NAME=$1

if [ -z "$FEATURE_NAME" ]; then
    echo "Usage: ./create_feature.sh <feature_name>"
    exit 1
fi

echo "🚀 Creando feature: $FEATURE_NAME"

mkdir -p "src/features/$FEATURE_NAME"
mkdir -p "src/features/$FEATURE_NAME/domain/entities"
mkdir -p "src/features/$FEATURE_NAME/domain/value_objects"
mkdir -p "src/features/$FEATURE_NAME/domain/services"
mkdir -p "src/features/$FEATURE_NAME/domain/exceptions"
mkdir -p "src/features/$FEATURE_NAME/domain/events"
mkdir -p "src/features/$FEATURE_NAME/application/use_cases"
mkdir -p "src/features/$FEATURE_NAME/application/interfaces/repositories"
mkdir -p "src/features/$FEATURE_NAME/application/interfaces/services"
mkdir -p "src/features/$FEATURE_NAME/application/dto"
mkdir -p "src/features/$FEATURE_NAME/application/mappers"
mkdir -p "src/features/$FEATURE_NAME/infrastructure/repositories"
mkdir -p "src/features/$FEATURE_NAME/infrastructure/services/security"
mkdir -p "src/features/$FEATURE_NAME/infrastructure/models"
mkdir -p "src/features/$FEATURE_NAME/presentation/api/v1/endpoints"
mkdir -p "src/features/$FEATURE_NAME/presentation/api/v1/schemas"
mkdir -p "src/features/$FEATURE_NAME/presentation/api/v1/dependencies"

# Crear __init__.py
# Crear todos los archivos
touch "src/features/$FEATURE_NAME/__init__.py"
touch "src/features/$FEATURE_NAME/domain/__init__.py"
touch "src/features/$FEATURE_NAME/domain/entities/__init__.py"
touch "src/features/$FEATURE_NAME/domain/value_objects/__init__.py"
touch "src/features/$FEATURE_NAME/domain/services/__init__.py"
touch "src/features/$FEATURE_NAME/domain/exceptions/__init__.py"
touch "src/features/$FEATURE_NAME/domain/events/__init__.py"
touch "src/features/$FEATURE_NAME/application/__init__.py"
touch "src/features/$FEATURE_NAME/application/use_cases/__init__.py"
touch "src/features/$FEATURE_NAME/application/interfaces/__init__.py"
touch "src/features/$FEATURE_NAME/application/interfaces/repositories/__init__.py"
touch "src/features/$FEATURE_NAME/application/interfaces/services/__init__.py"
touch "src/features/$FEATURE_NAME/application/dto/__init__.py"
touch "src/features/$FEATURE_NAME/application/mappers/__init__.py"
touch "src/features/$FEATURE_NAME/infrastructure/__init__.py"
touch "src/features/$FEATURE_NAME/infrastructure/repositories/__init__.py"
touch "src/features/$FEATURE_NAME/infrastructure/services/__init__.py"
touch "src/features/$FEATURE_NAME/infrastructure/services/security/__init__.py"
touch "src/features/$FEATURE_NAME/infrastructure/models/__init__.py"
touch "src/features/$FEATURE_NAME/presentation/__init__.py"
touch "src/features/$FEATURE_NAME/presentation/api/__init__.py"
touch "src/features/$FEATURE_NAME/presentation/api/v1/__init__.py"
touch "src/features/$FEATURE_NAME/presentation/api/v1/endpoints/__init__.py"
touch "src/features/$FEATURE_NAME/presentation/api/v1/schemas/__init__.py"
touch "src/features/$FEATURE_NAME/presentation/api/v1/dependencies/__init__.py"

# Crear archivo de blueprint
cat > "src/features/$FEATURE_NAME/presentation/api/v1/endpoints/__init__.py" << EOF
from flask import Blueprint

${FEATURE_NAME}_bp = Blueprint(
    '${FEATURE_NAME}',
    __name__,
    url_prefix='/api/v1/${FEATURE_NAME}'
)

# Importar rutas
from . import routes

__all__ = ['${FEATURE_NAME}_bp']
EOF

echo "✅ Feature '$FEATURE_NAME' creada!"
echo "📁 Estructura en: src/features/$FEATURE_NAME/"