"""Códigos de error de autenticación.

Centraliza los posibles resultados de error del flujo de autenticación para que
tanto los casos de uso como la capa de presentación (endpoints) hablen el mismo
lenguaje. Cada código tiene asociado un status HTTP y un mensaje por defecto en
español que el frontend puede mostrar o reinterpretar.
"""
from enum import Enum


class AuthErrorCode(str, Enum):
    """Códigos de error específicos del dominio de autenticación."""

    EMPTY_FIELDS = "EMPTY_FIELDS"
    INVALID_EMAIL = "INVALID_EMAIL"
    EMAIL_NOT_REGISTERED = "EMAIL_NOT_REGISTERED"
    INVALID_PASSWORD = "INVALID_PASSWORD"
    ACCOUNT_DISABLED = "ACCOUNT_DISABLED"
    ACCOUNT_LOCKED = "ACCOUNT_LOCKED"
    SERVER_ERROR = "SERVER_ERROR"


# Mapa de código -> status HTTP apropiado
AUTH_ERROR_STATUS = {
    AuthErrorCode.EMPTY_FIELDS: 400,
    AuthErrorCode.INVALID_EMAIL: 422,
    AuthErrorCode.EMAIL_NOT_REGISTERED: 404,
    AuthErrorCode.INVALID_PASSWORD: 401,
    AuthErrorCode.ACCOUNT_DISABLED: 403,
    AuthErrorCode.ACCOUNT_LOCKED: 423,
    AuthErrorCode.SERVER_ERROR: 500,
}

# Mensajes por defecto (español). El frontend puede reinterpretarlos por código.
AUTH_ERROR_MESSAGES = {
    AuthErrorCode.EMPTY_FIELDS: "Todos los campos son obligatorios.",
    AuthErrorCode.INVALID_EMAIL: "El formato del correo electrónico no es válido.",
    AuthErrorCode.EMAIL_NOT_REGISTERED: "El correo electrónico no está registrado.",
    AuthErrorCode.INVALID_PASSWORD: "La contraseña es incorrecta.",
    AuthErrorCode.ACCOUNT_DISABLED: "Tu cuenta está desactivada. Contacta al soporte.",
    AuthErrorCode.ACCOUNT_LOCKED: (
        "Tu cuenta ha sido bloqueada temporalmente por múltiples intentos fallidos."
    ),
    AuthErrorCode.SERVER_ERROR: (
        "Ocurrió un error en el servidor. Intenta nuevamente más tarde."
    ),
}


def build_auth_error(code: AuthErrorCode):
    """Devuelve (payload, status) listo para serializar en el endpoint."""
    message = AUTH_ERROR_MESSAGES[code]
    payload = {
        "error_code": code.value,
        "message": message,
        # 'error' se mantiene por compatibilidad con clientes antiguos
        "error": message,
    }
    return payload, AUTH_ERROR_STATUS[code]
