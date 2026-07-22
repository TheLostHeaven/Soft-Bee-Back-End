from dotenv import load_dotenv
import os

load_dotenv()

environment = os.getenv('FLASK_ENV', 'local')

env_file = f'.env.{environment}'
if os.path.exists(env_file):
    load_dotenv(env_file, override=True)

DATABASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    MAIL_SERVER = os.getenv("SMTP_HOST", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("SMTP_PORT") or 587)
    MAIL_USERNAME = os.getenv("SMTP_USER")
    MAIL_PASSWORD = os.getenv("SMTP_PASSWORD")
    MAIL_USE_TLS = True
    MAIL_DEFAULT_SENDER = os.getenv("SMTP_USER")

    EMAIL = {
        "smtp_host": MAIL_SERVER,
        "smtp_port": MAIL_PORT,
        "smtp_user": MAIL_USERNAME,
        "smtp_password": MAIL_PASSWORD,
        "from_email": MAIL_DEFAULT_SENDER
    }

    AUTH = {
        "password_algorithm": "argon2",
        "jwt_secret_key": os.getenv("JWT_KEY", "secret-key-default"),
        "jwt_algorithm": os.getenv("ALGORITHM", "HS256"),
        "jwt_issuer": os.getenv("JWT_ISSUER", "softbee-api"),
        "jwt_audience": os.getenv("JWT_AUDIENCE", "softbee-app"),
        "password_argon2_time_cost": int(os.getenv("ARGON2_TIME_COST") or 2),
        "password_argon2_memory_cost": int(os.getenv("ARGON2_MEMORY_COST") or 512000),
        "password_argon2_parallelism": int(os.getenv("ARGON2_PARALLELISM") or 2),
        "password_argon2_hash_len": int(os.getenv("ARGON2_HASH_LEN") or 32),
        "password_argon2_salt_len": int(os.getenv("ARGON2_SALT_LEN") or 16),
    }

    AI = {
        "openai_api_key": os.getenv("OPENAI_API_KEY"),
        "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY"),
        "gemini_api_key": os.getenv("GEMINI_API_KEY"),
        "deepseek_api_key": os.getenv("DEEPSEEK_API_KEY"),
        "default_provider": os.getenv("DEFAULT_AI_PROVIDER", "mock")
    }

    JWT_SECRET_KEY = AUTH["jwt_secret_key"]
    JWT_ALGORITHM = AUTH["jwt_algorithm"]  # <-- Esto ahora tiene valor
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("EXPIRES_TOKEN_SESSION") or 1440)  # 24 horas
    JWT_RESET_TOKEN_EXPIRES = int(os.getenv("EXPIRES_TOKEN_EMAIL") or 30)  # 30 minutos
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
    BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")

class LocalConfig(Config):
    """Configuración para entorno local"""
    DEBUG = True
    TESTING = False
    DATABASE_URL = os.getenv("DATABASE_URL")
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
    BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")

class DevelopmentConfig(Config):
    """Configuración para entorno de desarrollo (servidor de desarrollo)"""
    DEBUG = True
    TESTING = False
    DATABASE_URL = os.getenv("DATABASE_URL")

class ProductionConfig(Config):
    """Configuración para entorno de producción"""
    DEBUG = False
    TESTING = False
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL es requerida en producción")
    if not os.getenv("JWT_KEY"):
        raise ValueError("JWT_KEY es requerida en producción")
    if not os.getenv("SECRET_KEY"):
        raise ValueError("SECRET_KEY es requerida en producción")

class TestingConfig(Config):
    """Configuración para pruebas"""
    DEBUG = True
    TESTING = True
    DATABASE_URL = os.getenv("DATABASE_URL")
    WTF_CSRF_ENABLED = False

config = {
    'local': LocalConfig,
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': LocalConfig
}

def get_config():
    """Obtiene la configuración basada en la variable de entorno FLASK_ENV"""
    env = os.getenv('FLASK_ENV', 'local')
    return config.get(env, config['default'])