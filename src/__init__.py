# src/__init__.py
import os
from flask import Flask
from flask_cors import CORS
from src.core.database.db import db, init_app as init_db
from src.core.dependencies.containers import MainContainer
from config import Config as get_config

def create_app(config_class=None):
    """Factory para crear la aplicación Flask"""
    app = Flask(__name__)
    
    # Cargar configuración
    if config_class is None:
        config_class = get_config()
    
    app.config.from_object(config_class)
    
    # Configurar CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": app.config.get('FRONTEND_URL', 'http://localhost:3000'),
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization", "Accept"],
            "expose_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })
    
    # Inicializar base de datos
    init_db(app)
    
    # Configurar logging
    if app.config.get('DEBUG'):
        app.logger.setLevel('DEBUG')
    else:
        app.logger.setLevel('INFO')
    
    # Configurar contenedor DI
    container = MainContainer()
    
    # Configurar desde el objeto de configuración de Flask
    container.config.AUTH.jwt_secret_key.from_value(
        app.config.get('jwt_secret_key', app.config.get('AUTH', {}).get('jwt_secret_key', 'secret'))
    )
    container.config.AUTH.jwt_algorithm.from_value(
        app.config.get('jwt_algorithm', app.config.get('AUTH', {}).get('jwt_algorithm', 'HS256'))
    )
    
    # Configurar Argon2
    container.config.AUTH.password_argon2_time_cost.from_value(
        app.config.get('AUTH', {}).get('password_argon2_time_cost', 2)
    )
    container.config.AUTH.password_argon2_memory_cost.from_value(
        app.config.get('AUTH', {}).get('password_argon2_memory_cost', 512000)
    )
    container.config.AUTH.password_argon2_parallelism.from_value(
        app.config.get('AUTH', {}).get('password_argon2_parallelism', 2)
    )
    container.config.AUTH.password_argon2_hash_len.from_value(
        app.config.get('AUTH', {}).get('password_argon2_hash_len', 32)
    )
    container.config.AUTH.password_argon2_salt_len.from_value(
        app.config.get('AUTH', {}).get('password_argon2_salt_len', 16)
    )
    
    # Configurar email
    container.config.EMAIL.smtp_server.from_value(app.config.get('MAIL_SERVER', 'smtp.gmail.com'))
    container.config.EMAIL.smtp_port.from_value(app.config.get('MAIL_PORT', 587))
    container.config.EMAIL.sender_email.from_value(app.config.get('MAIL_USERNAME', ''))
    container.config.EMAIL.sender_password.from_value(app.config.get('MAIL_PASSWORD', ''))
    
    # Conectar DI a los módulos
    container.wire(
        modules=[
            "src.features.auth.presentation.api.v1.endpoints.auth",
            "src.features.apiaries.presentation.api.v1.endpoints.apiaries",
        ]
    )
    
    # Registrar blueprints
    register_blueprints(app)
    
    return app

def register_blueprints(app):
    """Registra todos los blueprints"""
    # Auth
    from src.features.auth.presentation.api.v1.endpoints.auth import auth_bp
    app.register_blueprint(auth_bp)
    
    # Apiaries
    from src.features.apiaries.presentation.api.v1.endpoints.apiary_endpoints import apiaries_bp
    app.register_blueprint(apiaries_bp)
    
    app.logger.info("Blueprints registrados correctamente")