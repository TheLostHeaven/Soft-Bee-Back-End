import os
from flask import g, current_app
import psycopg2
from urllib.parse import quote_plus
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session, Session
from flask_migrate import Migrate

# Instancia global de SQLAlchemy para migraciones
db = SQLAlchemy()
migrate = Migrate()
Base = declarative_base()

def get_db() -> Session:
    """Retorna la sesión de SQLAlchemy gestionada por Flask-SQLAlchemy"""
    return db.session

def init_app(app):
    """Inicializa la base de datos con la aplicación Flask"""
    
    # Configurar SQLAlchemy para migraciones
    database_url = app.config.get('DATABASE_URL')
    
    if not database_url:
        raise ValueError("DATABASE_URL no está configurada")

    # Reemplazar 'postgres://' con 'postgresql://' para compatibilidad con SQLAlchemy
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    # Agregar SSL si es necesario
    sslmode_require = os.getenv('SSL_MODE', '') == 'require'
    if sslmode_require and 'sslmode=' not in database_url:
        separator = '?' if '?' not in database_url else '&'
        database_url += f"{separator}sslmode=require"

    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar SQLAlchemy y Flask-Migrate
    db.init_app(app)
    migrate.init_app(app, db)
    
    @app.teardown_appcontext
    def teardown_db(exception=None):
        """Asegura que la sesión de la base de datos se cierre después de cada solicitud."""
        session = db.session
        try:
            if exception is None:
                session.commit()
        except Exception as e:
            session.rollback()
            # Optionally log the exception e
            raise
        finally:
            session.remove()
    
    with app.app_context():
        # Mostrar información del entorno y base de datos
        env = os.getenv('FLASK_ENV', 'local')
        config_name = app.config.__class__.__name__
        db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
        
        print(f"🚀 Iniciando aplicación en entorno: {env}")
        print(f"⚙️  Configuración activa: {config_name}")
        
        if db_uri.startswith('postgresql'):
            db_type = 'PostgreSQL'
            # Ocultar credenciales en la URL para seguridad
            safe_uri = db_uri.split('@')[-1] if '@' in db_uri else db_uri
            print(f"📂 Usando base de datos: {db_type}")
        else:
            print(f"🚀 Iniciando aplicación en entorno: {env}")
            print(f"📂 Usando base de datos: desconocida")
            
        # Para depuración: mostrar la URL completa de la base de datos si el entorno es local o de desarrollo
        if env in ['local', 'development']:
            print(f"🔎 DEBUG - DATABASE_URL (completa): {app.config.get('SQLALCHEMY_DATABASE_URI')}")

        print(f"🌐 URLs configuradas:")
        print(f"   Frontend: {app.config.get('FRONTEND_URL')}")
        print(f"   Backend: {app.config.get('BASE_URL')}")
        print(f"🐛 Debug mode: {app.config.get('DEBUG', False)}")

        # Solo crear tablas automáticamente si no existen migraciones
        migrations_dir = os.path.join(app.root_path, 'migrations')
        if not os.path.exists(migrations_dir):
            print(" No se encontraron migraciones, creando tablas automáticamente...")
            try:
                # Importar modelos para que SQLAlchemy los detecte
                from src.features.auth.infrastructure.models.user_model import UserModel
                from src.features.apiaries.infrastructure.models.apiary_model import ApiaryModel
                from src.features.questions.infrastructure.models.question_models import ApiaryQuestionModel
                
                db.create_all()
                print("✅ Tablas de base de datos inicializadas correctamente")
            except Exception as e:
                print(f"❌ Error al inicializar tablas: {e}")
                raise
        else:
            print("📋 Migraciones encontradas, usar 'flask db upgrade' para aplicar cambios")
