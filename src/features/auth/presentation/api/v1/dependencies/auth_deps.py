import logging
from functools import wraps
from flask import request, jsonify, g
from typing import Optional

logger = logging.getLogger(__name__)
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

@inject
def token_required(
    user_repository: IUserRepository = Provide[Container.auth_user_repository],
    jwt_service: JWTService = Provide[Container.jwt_service]
):
    """Decorator para requerir token JWT válido"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Dejar pasar el preflight CORS sin exigir token.
            # El navegador envía OPTIONS sin header Authorization, por lo que
            # la validación de token no debe aplicarse a estas peticiones.
            if request.method == 'OPTIONS':
                return '', 204

            auth_header = request.headers.get('Authorization')

            # LOGGING TEMPORAL: diagnostica el motivo exacto de un 401.
            # Se enmascara el token para no filtrar credenciales en los logs.
            masked = None
            if auth_header:
                _p = auth_header.split()
                masked = f"{_p[0]} {_p[1][:8]}...({len(_p[1])} chars)" if len(_p) == 2 else auth_header[:20]
            logger.info("[token_required] %s %s Authorization=%s",
                        request.method, request.path, masked or "<AUSENTE>")

            if not auth_header:
                logger.warning("[token_required] RECHAZO: header Authorization ausente")
                return jsonify({"error": "Missing authorization header"}), 401
            
            # Verificar formato "Bearer <token>"
            parts = auth_header.split()
            if len(parts) != 2 or parts[0].lower() != 'bearer':
                logger.warning("[token_required] RECHAZO: formato de header inválido (parts=%d)", len(parts))
                return jsonify({"error": "Invalid authorization header format"}), 401
            
            token = parts[1]
            
            # Decodificar y verificar token
            try:
                payload = jwt_service.decode_token(token)
            except (ValueError, Exception) as e:
                logger.warning("[token_required] RECHAZO: token inválido o expirado (%s: %s)",
                               type(e).__name__, e)
                return jsonify({"error": "Invalid or expired token"}), 401
            
            # Verificar tipo de token
            if payload.get('type') != 'access':
                logger.warning("[token_required] RECHAZO: tipo de token inválido (type=%s)", payload.get('type'))
                return jsonify({"error": "Invalid token type"}), 401
            
            # Obtener usuario
            user_id = payload.get('sub')
            if not user_id:
                logger.warning("[token_required] RECHAZO: claim 'sub' ausente en el payload")
                return jsonify({"error": "Invalid token payload"}), 401
            
            user = user_repository.find_by_id(user_id)
            if not user or not user.is_active:
                logger.warning("[token_required] RECHAZO: usuario no encontrado o inactivo (sub=%s)", user_id)
                return jsonify({"error": "User not found or inactive"}), 401
            
            # Agregar al contexto
            g.current_user = user
            g.current_user_id = user_id
            g.token_payload = payload

            logger.info("[token_required] OK: acceso concedido (sub=%s)", user_id)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@inject
def admin_required(
    user_repository: IUserRepository = Provide[Container.auth_user_repository],
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
            user_repository: IUserRepository = Provide[Container.auth_user_repository],
            jwt_service: JWTService = Provide[Container.jwt_service],
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