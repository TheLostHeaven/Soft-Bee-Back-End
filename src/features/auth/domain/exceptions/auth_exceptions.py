"""Excepciones específicas del dominio de autenticación"""

class AuthException(Exception):
    """Excepción base para el dominio de autenticación"""
    def __init__(self, message: str, code: str = "AUTH_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)

class InvalidEmailException(AuthException):
    """Email inválido"""
    def __init__(self, message: str = "Invalid email address"):
        super().__init__(message, "INVALID_EMAIL")

class WeakPasswordException(AuthException):
    """Password débil"""
    def __init__(self, message: str = "Password is too weak"):
        super().__init__(message, "WEAK_PASSWORD")

class InvalidUserException(AuthException):
    """Usuario inválido"""
    def __init__(self, message: str = "Invalid user data"):
        super().__init__(message, "INVALID_USER")

class UserNotFoundException(AuthException):
    """Usuario no encontrado"""
    def __init__(self, message: str = "User not found"):
        super().__init__(message, "USER_NOT_FOUND")

class InvalidCredentialsException(AuthException):
    """Credenciales inválidas"""
    def __init__(self, message: str = "Invalid credentials"):
        super().__init__(message, "INVALID_CREDENTIALS")

class AccountLockedException(AuthException):
    """Cuenta bloqueada"""
    def __init__(self, message: str = "Account is locked"):
        super().__init__(message, "ACCOUNT_LOCKED")

class TokenExpiredException(AuthException):
    """Token expirado"""
    def __init__(self, message: str = "Token has expired"):
        super().__init__(message, "TOKEN_EXPIRED")

class InvalidTokenException(AuthException):
    """Token inválido"""
    def __init__(self, message: str = "Invalid token"):
        super().__init__(message, "INVALID_TOKEN")

class EmailAlreadyExistsException(AuthException):
    """Email ya registrado"""
    def __init__(self, message: str = "Email already exists"):
        super().__init__(message, "EMAIL_EXISTS")


class InvalidResetTokenException(AuthException):
    """Excepción cuando el token de reseteo es inválido o ha expirado"""
    pass

class PasswordResetException(AuthException):
    """Excepción cuando hay un error en el proceso de reseteo de contraseña"""
    pass

class PasswordValidationException(AuthException):
    """Excepción cuando la contraseña no cumple los requisitos"""
    pass    