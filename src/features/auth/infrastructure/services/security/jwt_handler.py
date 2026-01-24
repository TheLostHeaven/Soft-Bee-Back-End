from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from jose import jwt
from ....application.interfaces.services.token_service import ITokenService

class JWTService(ITokenService):
    """Implementación del servicio de tokens JWT"""
    
    def __init__(
        self,
        secret_key: str,
        algorithm: str = "HS256",
        issuer: Optional[str] = None,
        audience: Optional[str] = None
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.issuer = issuer
        self.audience = audience

    def create_access_token(self, data: Dict[str, Any], expires_in: int = 900) -> str:
        """Crear access token JWT con diccionario"""
        to_encode = data.copy()
        
        now = datetime.utcnow()
        expire = now + timedelta(seconds=expires_in)
        
        to_encode.update({
            "exp": expire,
            "iat": now,
            "nbf": now,
            "type": "access"
        })
        
        if self.issuer:
            to_encode["iss"] = self.issuer
        if self.audience:
            to_encode["aud"] = self.audience
        
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    
    def generate_access_token(self, user_id: str, email: str, expires_in: int = 3600) -> str:
        """Crear access token JWT con user_id y email"""
        data = {
            "sub": user_id,
            "email": email,
            "user_id": user_id
        }
        return self.create_access_token(data, expires_in)
    
    def create_refresh_token(self, data: Dict[str, Any], expires_in: int = 2592000) -> str:
        """Crear refresh token JWT con diccionario"""
        to_encode = data.copy()  # ¡Aquí está el otro .copy()!
        
        now = datetime.utcnow()
        expire = now + timedelta(seconds=expires_in)
        
        to_encode.update({
            "exp": expire,
            "iat": now,
            "nbf": now,
            "type": "refresh"
        })
        
        if self.issuer:
            to_encode["iss"] = self.issuer
        if self.audience:
            to_encode["aud"] = self.audience
        
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    
    def generate_refresh_token(self, user_id: str, email: str, expires_in: int = 2592000) -> str:
        """Crear refresh token JWT con user_id y email"""
        data = {
            "sub": user_id,
            "email": email,
            "user_id": user_id
        }
        return self.create_refresh_token(data, expires_in)
    
    def decode_token(self, token: str) -> Dict[str, Any]:
        """Decodificar token JWT"""
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
                issuer=self.issuer,
                audience=self.audience
            )
            return payload
        except Exception as e:
            raise ValueError(f"Invalid token: {str(e)}")
    
    def verify_token(self, token: str) -> bool:
        """Verificar si un token es válido"""
        try:
            self.decode_token(token)
            return True
        except:
            return False
        
    def generate_reset_token(self) -> str:
        """Generar token de reseteo de contraseña"""
        import secrets
        # Generar token seguro de 32 caracteres
        return secrets.token_urlsafe(32)