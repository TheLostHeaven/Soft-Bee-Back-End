#!/bin/bash
# init_project.sh

echo "🚀 Inicializando proyecto Flask con Arquitectura Limpia"

# 1. Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no encontrado. Instala Python 3.10 o superior."
    exit 1
fi

# 2. Crear estructura si no existe
echo "📁 Creando estructura de directorios..."
mkdir -p src/{domain,application,infrastructure,api,shared}
mkdir -p tests/{unit,integration,fixtures}
mkdir -p logs

# 3. Crear virtual environment
echo "🐍 Creando virtual environment..."
python -m venv venv

# 4. Activar y instalar
echo "📦 Instalando dependencias..."
source venv/Scripts/activate

# 5. Instalar base primero
echo "📚 Instalando dependencias base..."
pip install -r requirements/base.txt

# 6. Preguntar por entorno adicional
read -p "¿Instalar dependencias de desarrollo también? (s/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo "🔧 Instalando desarrollo..."
    pip install -r requirements/development.txt
fi

# 7. Configurar pre-commit hooks
if [ -f ".pre-commit-config.yaml" ]; then
    echo "🔨 Configurando pre-commit hooks..."
    pre-commit install
fi

echo "✅ ¡Proyecto inicializado correctamente!"
echo ""
echo "📋 Comandos útiles:"
echo "   source venv/Scripts/activate    # Activar entorno virtual"
echo "   make install-dev            # Instalar dependencias dev"
echo "   make test                   # Ejecutar tests"
echo "   make docker-up              # Levantar con Docker"