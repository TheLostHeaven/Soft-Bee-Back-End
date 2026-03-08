# src/features/auth/infrastructure/services/password_service_impl.py
import secrets
import string
from datetime import datetime, timedelta
from typing import Tuple, Dict, Any, Optional
from argon2 import PasswordHasher, exceptions as argon2_exceptions
from jose import JWTError, jwt
import logging

logger = logging.getLogger(__name__)

class PasswordServiceImpl:
    """Servicio de contraseñas con Argon2 y JWT"""
    
    def __init__(self, 
                 secret_key: str = None,
                 algorithm: str = "HS256",
                 time_cost: int = None,
                 memory_cost: int = None,
                 parallelism: int = None,
                 hash_len: int = None,
                 salt_len: int = None):
        """
        Constructor robusto que maneja valores None
        """
        self.secret_key = secret_key or "default-secret-key-change-in-production"
        self.algorithm = algorithm
        
        time_cost = time_cost or 2
        memory_cost = memory_cost or 512 * 1024  # 512 MB en KiB
        parallelism = parallelism or 2
        hash_len = hash_len or 32
        salt_len = salt_len or 16
        
        if secret_key == "default-secret-key-change-in-production":
            logger.warning("⚠️ USING DEFAULT SECRET KEY - CHANGE IN PRODUCTION!")
        
        logger.info(f"🔐 Initializing PasswordServiceImpl")
        
        self.password_hasher = PasswordHasher(
            time_cost=time_cost,
            memory_cost=memory_cost,
            parallelism=parallelism,
            hash_len=hash_len,
            salt_len=salt_len
        )
    def hash_password(self, password: str) -> str:
        """
        Hashea una contraseña usando Argon2
        
        Args:
            password: Contraseña en texto plano
            
        Returns:
            str: Hash de la contraseña
        """
        try:
            hashed = self.password_hasher.hash(password)
            logger.debug(f"Password hashed successfully")
            return hashed
        except Exception as e:
            logger.error(f"Error hashing password: {str(e)}")
            raise ValueError(f"Error hashing password: {str(e)}")
        
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """
        Verifica una contraseña contra su hash
        
        Args:
            password: Contraseña en texto plano
            hashed_password: Hash almacenado
            
        Returns:
            bool: True si es válida, False en caso contrario
        """
        try:
            is_valid = self.password_hasher.verify(hashed_password, password)
            return is_valid
        except argon2_exceptions.VerifyMismatchError:
            logger.debug("Password verification failed: mismatch")
            return False
        except Exception as e:
            logger.error(f"Error verifying password: {str(e)}")
            return False
        
    def generate_jwt_token(self, payload: Dict[str, Any], expires_minutes: int = 30) -> str:
        """Genera un token JWT"""
        try:
            payload_copy = payload.copy()
            now = datetime.utcnow()
            expire = now + timedelta(minutes=expires_minutes)
            
            payload_copy.update({
                "exp": expire,
                "iat": now,
                "nbf": now,
            })
            
            token = jwt.encode(
                payload_copy,
                self.secret_key,
                algorithm=self.algorithm
            )
            
            return token
            
        except Exception as e:
            logger.error(f"Error generating JWT token: {str(e)}")
            raise
    
    def verify_jwt_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verifica un token JWT"""
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )
            return payload
        except JWTError:
            return None