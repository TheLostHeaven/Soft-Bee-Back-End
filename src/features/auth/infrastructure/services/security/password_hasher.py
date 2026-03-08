import argon2
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class PasswordHasher:
    """Servicio para hash y verificación de contraseñas usando Argon2"""
    
    def __init__(self, time_cost=2, memory_cost=512000, parallelism=2, 
                hash_len=32, salt_len=16):
        """
        Inicializa el hasher de contraseñas con Argon2
        
        Args:
            time_cost: Número de iteraciones (mayor = más seguro pero más lento)
            memory_cost: Memoria en KB a usar
            parallelism: Número de hilos paralelos
            hash_len: Longitud del hash en bytes
            salt_len: Longitud de la sal en bytes
        """
        self.time_cost = time_cost
        self.memory_cost = memory_cost
        self.parallelism = parallelism
        self.hash_len = hash_len
        self.salt_len = salt_len
        
        self.hasher = argon2.PasswordHasher(
            time_cost=time_cost,
            memory_cost=memory_cost,
            parallelism=parallelism,
            hash_len=hash_len,
            salt_len=salt_len
        )
        
        logger.info(f"PasswordHasher initialized with Argon2 - "
                f"time_cost: {time_cost}, memory_cost: {memory_cost}KB")
    
    def hash_password(self, password: str) -> str:
        """Genera hash de una contraseña usando Argon2"""
        try:
            start_time = datetime.now()
            hashed = self.hasher.hash(password)
            elapsed = (datetime.now() - start_time).total_seconds()
            
            logger.debug(f"Password hashed in {elapsed:.3f}s")
            return hashed
            
        except Exception as e:
            logger.error(f"Error hashing password: {str(e)}")
            raise
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verifica si una contraseña coincide con el hash almacenado"""
        try:
            start_time = datetime.now()
            is_valid = self.hasher.verify(hashed_password, password)
            elapsed = (datetime.now() - start_time).total_seconds()
            
            logger.debug(f"Password verified in {elapsed:.3f}s")
            return is_valid
            
        except argon2.exceptions.VerifyMismatchError:
            logger.warning("Password verification failed - mismatch")
            return False
        except argon2.exceptions.VerificationError as e:
            logger.error(f"Password verification error: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error verifying password: {str(e)}")
            return False
    
    def needs_rehash(self, hashed_password: str) -> bool:
        """Verifica si un hash necesita ser rehasheado (si los parámetros cambiaron)"""
        try:
            return self.hasher.check_needs_rehash(hashed_password)
        except Exception as e:
            logger.error(f"Error checking if password needs rehash: {str(e)}")
            return False