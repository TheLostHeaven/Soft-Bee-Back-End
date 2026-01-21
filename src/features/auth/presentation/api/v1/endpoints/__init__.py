# src/features/auth/presentation/api/v1/endpoints/__init__.py

# Exponer el blueprint desde el módulo de endpoints de autenticación
from .auth import auth_bp

__all__ = ['auth_bp']