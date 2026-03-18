# src/api/router.py
from flask import Flask, Blueprint
from typing import List, Dict, Optional

class FeatureRouter:
    """Router que registra todas las features de forma modular"""
    
    def __init__(self, app: Flask):
        self.app = app
        self.registered_features: List[str] = []
    
    def register(self, feature_name: str, enabled: bool = True) -> bool:
        """
        Registra los blueprints asociados a una feature.
        Busca dinámicamente objetos de tipo Blueprint en el módulo de endpoints.
        """
        if not enabled:
            return False
            
        try:
            # 1. Importar el módulo de endpoints de la feature
            module_name = f"src.features.{feature_name}.presentation.api.v1.endpoints"
            module = __import__(module_name, fromlist=[''])

            # 2. Definir los nombres posibles de los Blueprints en el sistema
            potential_names = [
                f'{feature_name}_bp',
                'auth_bp',
                'api_bp',
                'user_bp',
                'beehive_bp',
                'inventory_bp',
                'ai_agent_bp',
                'maya_voice_bp',
                'questions_bp',
                'answers_bp',
                'treatments_bp',
                'bp',
            ]

            # 3. Buscar y registrar todos los blueprints que existan en el módulo
            registered_any = False
            for bp_name in potential_names:
                if hasattr(module, bp_name):
                    found_bp = getattr(module, bp_name)
                    # Verificar que sea un objeto Blueprint de Flask
                    if found_bp and isinstance(found_bp, Blueprint):
                        # Evitar doble registro si el nombre ya existe
                        if found_bp.name not in self.app.blueprints:
                            try:
                                self.app.register_blueprint(found_bp)
                                registered_any = True
                                print(f"✅ Blueprint registrado: {feature_name} -> {bp_name} ({found_bp.name})")
                            except Exception as e:
                                print(f"⚠️ Error registrando blueprint {bp_name} en {feature_name}: {str(e)}")
            
            # 4. Confirmar registro exitoso
            if registered_any:
                self.registered_features.append(feature_name)
                return True
            else:
                return False
                
        except ImportError:
            # El módulo de la feature no tiene endpoints definidos
            return False
        except Exception as e:
            print(f"❌ Error registrando feature {feature_name}: {str(e)}")
            return False

    def register_many(self, features_config: Dict[str, bool]) -> List[str]:
        """Registrar múltiples features basándose en un diccionario de configuración"""
        successful = []
        for feature_name, enabled in features_config.items():
            if self.register(feature_name, enabled):
                successful.append(feature_name)
        return successful
    
    @property
    def features(self) -> List[str]:
        """Obtener lista de features registradas exitosamente"""
        return self.registered_features.copy()

def register_features(app: Flask, features: List[str]) -> List[str]:
    """
    Función helper de alto nivel para registrar una lista de nombres de features.
    """
    router = FeatureRouter(app)
    features_config = {name: True for name in features}
    return router.register_many(features_config)
