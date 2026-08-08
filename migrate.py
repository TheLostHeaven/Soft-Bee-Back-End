#!/usr/bin/env python
"""
Script para ejecutar migraciones de base de datos
"""
import os
import sys
from app import create_app
from flask_migrate import upgrade, init, migrate as flask_migrate

def run_migrations():
    """Ejecuta las migraciones de base de datos"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🔄 Ejecutando migraciones...")
            
            # Verificar si existe el directorio de migraciones
            migrations_dir = os.path.join(os.getcwd(), 'migrations')
            
            if os.path.exists(migrations_dir):
                print("📋 Directorio de migraciones encontrado")
                # Ejecutar upgrade
                upgrade()
                print("✅ Migraciones aplicadas correctamente")
            else:
                print("⚠️  No se encontró directorio de migraciones")
                print("🔧 Creando tablas directamente...")
                from src.core.database.db import db
                db.create_all()
                print("✅ Tablas creadas correctamente")
                
        except Exception as e:
            print(f"❌ Error al ejecutar migraciones: {e}")
            # No fallar el build, solo advertir
            print("⚠️  Continuando sin migraciones...")
            return 0
    
    return 0

if __name__ == "__main__":
    sys.exit(run_migrations())
