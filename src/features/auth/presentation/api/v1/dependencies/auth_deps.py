from functools import wraps
from flask import request, jsonify, g
from typing import Optional
from .....infrastructure.services.security.jwt_handler import JWTService
from .....application.interfaces.repositories.user_repository import IUserRepository
from dependency_injector.wiring import inject, Provide
from src.core.dependencies.containers import MainContainer as Container

def get_current_user():
    """Obtener usuario actual del contexto"""
    return getattr(g, 'current_user', None)

def get_current_user_id():
    """Obtener ID del usuario actual"""
    return getattr(g, 'current_user_id', None)

def token_required():
    """Decorator para requerir token JWT válido"""
    def decorator(f):
        @wraps(f)
        @inject
        def decorated_function(
            *args,
            user_repository: IUserRepository = Provide[Container.user_repository],
            jwt_service: JWTService = Provide[Container.jwt_service],
            **kwargs
        ):
            auth_header = request.headers.get('Authorization')
            
            if not auth_header:
                return jsonify({"error": "Missing authorization header"}), 401
            
            # Verificar formato "Bearer <token>"
            parts = auth_header.split()
            if len(parts) != 2 or parts[0].lower() != 'bearer':
                return jsonify({"error": "Invalid authorization header format"}), 401
            
            token = parts[1]
            
            # Verificar token
            payload = jwt_service.verify_token(token)
            if not payload:
                return jsonify({"error": "Invalid or expired token"}), 401
            
            # Verificar tipo de token
            if payload.get('type') != 'access':
                return jsonify({"error": "Invalid token type"}), 401
            
            # Obtener usuario
            user_id = payload.get('sub')
            if not user_id:
                return jsonify({"error": "Invalid token payload"}), 401
            
            user = user_repository.find_by_id(user_id)
            if not user or not user.is_active:
                return jsonify({"error": "User not found or inactive"}), 401
            
            # Agregar al contexto
            g.current_user = user
            g.current_user_id = user_id
            g.token_payload = payload
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@inject
def admin_required(
    user_repository: IUserRepository = Provide[Container.user_repository],
    jwt_service: JWTService = Provide[Container.jwt_service]
):
    """Decorator para requerir rol de admin"""
    def decorator(f):
        @wraps(f)
        @token_required(user_repository, jwt_service)
        def decorated_function(*args, **kwargs):
            user = get_current_user()
            
            # Aquí puedes agregar lógica para verificar rol de admin
            # Por ahora, solo verificamos si el usuario está verificado
            if not user.is_verified:
                return jsonify({"error": "Admin privileges required"}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def optional_token():
    """Decorator para token opcional (para endpoints públicos/privados)"""
    def decorator(f):
        @wraps(f)
        @inject
        def decorated_function(
            *args, 
            user_repository: IUserRepository = Provide[Container.auth.user_repository],
            jwt_service: JWTService = Provide[Container.auth.jwt_service],
            **kwargs
        ):
            auth_header = request.headers.get('Authorization')
            
            if auth_header:
                parts = auth_header.split()
                if len(parts) == 2 and parts[0].lower() == 'bearer':
                    token = parts[1]
                    payload = jwt_service.verify_token(token)
                    
                    if payload and payload.get('type') == 'access':
                        user_id = payload.get('sub')
                        if user_id:
                            user = user_repository.find_by_id(user_id)
                            if user and user.is_active:
                                g.current_user = user
                                g.current_user_id = user_id
                                g.token_payload = payload
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator