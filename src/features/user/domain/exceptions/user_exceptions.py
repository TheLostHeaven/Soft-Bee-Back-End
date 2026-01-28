"""Excepciones específicas del dominio de usuario"""

class UserException(Exception):
    """Excepción base para el dominio de usuario"""
    def __init__(self, message: str, code: str = "USER_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)

class UserNotFoundError(UserException):
    """Usuario no encontrado"""
    def __init__(self, message: str = "User not found"):
        super().__init__(message, "USER_NOT_FOUND")
