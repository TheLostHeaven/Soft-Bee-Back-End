# src/api/router.py
from flask import Flask
from typing import List, Dict, Optional, Callable

class FeatureRouter:
    """Router que registra todas las features"""
    
    def __init__(self, app: Flask):
        self.app = app
        self.registered_features: List[str] = []
    
    def register(self, feature_name: str, enabled: bool = True) -> bool:
        """Registrar una feature individual con depuración"""
        if not enabled:
            return False
        try:
            # 1. Importar la feature
            module_name = f"src.features.{feature_name}.presentation.api.v1.endpoints"
            module = __import__(module_name, fromlist=[''])


            # 2. Buscar y registrar blueprints
            registered_any = False
            for bp_name in blueprint_names:
                if hasattr(module, bp_name):
                    found_bp = getattr(module, bp_name)
                    if found_bp: # Asegurarse de que no es None
                        self.app.register_blueprint(found_bp)
                        registered_any = True
            
            # 3. Marcar como registrada si se encontró al menos uno
            if registered_any:
                self.registered_features.append(feature_name)
                return True
            else:
                return False
                
        except ImportError as e:
            return False
        except Exception as e:
            import traceback
            traceback.print_exc()
            return False

    def register_many(self, features_config: Dict[str, bool]) -> List[str]:
        """Registrar múltiples features"""
        successful = []
        for feature_name, enabled in features_config.items():
            if self.register(feature_name, enabled):
                successful.append(feature_name)
        return successful
    
    @property
    def features(self) -> List[str]:
        """Obtener features registradas"""
        return self.registered_features.copy()

# Función de conveniencia
def register_features(app: Flask, features: List[str]) -> List[str]:
    """
    Función helper para registrar features
    
    Args:
        app: Aplicación Flask
        features: Lista de nombres de features
        
    Returns:
        List[str]: Features registradas exitosamente
    """
    router = FeatureRouter(app)
    features_config = {name: True for name in features}
    return router.register_many(features_config)
