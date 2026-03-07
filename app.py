from flask import Flask
from flask_cors import CORS
from dependency_injector import providers
from src.shared.utils.file_handler import FileHandler
from src.core.database.db import init_app, get_db
from src.api.router import register_features
from config import get_config
from datetime import datetime
from flask.json.provider import DefaultJSONProvider 
import os
from src.core.dependencies.containers import MainContainer


class CustomJSONProvider(DefaultJSONProvider):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%S')
        return super().default(obj)

def create_app(config_name: str = None, features_config: dict = None, testing: bool = False):
    app = Flask(__name__, instance_relative_config=True)

    app.json_provider_class = CustomJSONProvider

    if testing:
        os.environ['FLASK_ENV'] = 'testing'
    
    config_class = get_config()
    app.config.from_object(config_class)

    # Dynamic CORS configuration
    origins = os.environ.get('CORS_ORIGINS')
    if origins:
        origins_list = [o.strip() for o in origins.split(',')]
        CORS(app, resources={
            r"/api/*": {
                "origins": origins_list,
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization", "Accept"],
                "expose_headers": ["Content-Type", "Authorization"],
                "supports_credentials": True
            }
        })
    else:
        # Default CORS configuration if the environment variable is not set
        CORS(app, resources={r"/api/*": {"origins": "*"}})

    file_handler = FileHandler()
    file_handler.init_app(app)
    app.file_handler = file_handler

    # Configure dependency injection
    container = MainContainer()
    container.config.from_dict(app.config)
    container.db_session.override(providers.Factory(get_db))
    container.wire(modules=["src.features.auth.presentation.api.v1.endpoints.auth",
                            "src.features.apiaries.presentation.api.v1.endpoints.apiary_endpoints",
                            "src.features.user.presentation.api.v1.endpoints.users",
                            "src.features.beehive.presentation.api.v1.endpoints.beehive_endpoints",
                            "src.features.inventory.presentation.api.v1.endpoints.inventory_endpoints",
                            "src.features.ai_agent.presentation.api.v1.endpoints.ai_agent",
                            "src.features.treatments.presentation.api.v1.endpoints.routes",
                            "src.features.questions.presentation.api.v1.endpoints.routes"])
    app.container = container

    # Inicializar base de datos y migraciones
    init_app(app)

    # from src.routes.health import create_health_routes
    # from src.routes.auth import create_auth_routes
    features_to_register = ['auth', 'apiaries', 'user', 'beehive', 'inventory', 'ai_agent', 'treatments', 'questions']
    registered_features = register_features(app, features_to_register)

    print("\n" + "="*50)
    print("🚀 Aplicación Flask iniciada")
    print("="*50)
    print("\n📋 Rutas registradas:")
    for rule in app.url_map.iter_rules():
        print(f"  {rule.methods} {rule.rule}")
    
    print("\n" + "="*50)

    # mail = Mail(app)
    # email_service = EmailService(mail)

    # with app.app_context():
        # auth_bp = create_auth_routes(get_db_func=get_db, email_service=email_service)
    #     app.register_blueprint(auth_bp, url_prefix='/api')

    # app.register_blueprint(create_health_routes(), url_prefix='/api')


    return app