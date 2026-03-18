# src/api/router.py
from flask import Flask
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
            # Se ha restaurado esta lista que se perdió en la refactorización anterior
            blueprint_names = [
                f'{feature_name}_bp',
                'auth_bp',
                'api_bp',
                'user_bp',
                'beehive_bp',
                'inventory_bp',
                'ai_agent_bp',
                'questions_bp',
                'answers_bp',
                'treatments_bp',
                'bp',
            ]

            # 3. Buscar y registrar todos los blueprints que existan en el módulo
            registered_any = False
            for bp_name in blueprint_names:
                if hasattr(module, bp_name):
                    found_bp = getattr(module, bp_name)
                    if found_bp: # Verificar que el objeto existe
                        self.app.register_blueprint(found_bp)
                        registered_any = True
                        # Debug print solicitado para verificar registro
                        print(f"✅ Blueprint registrado: {feature_name} -> {bp_name}")
            
            # 4. Confirmar registro exitoso
            if registered_any:
                self.registered_features.append(feature_name)
                return True
            else:
                # Si el módulo existe pero no tiene blueprints conocidos
                print(f"⚠️  Advertencia: No se encontraron blueprints en el módulo {feature_name}")
                return False
                
        except ImportError as e:
            # El módulo de la feature no tiene endpoints definidos
            return False
        except Exception as e:
            print(f"❌ Error registrando feature {feature_name}: {str(e)}")
            import traceback
            traceback.print_exc()
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
    
    Args:
        app: Instancia de la aplicación Flask.
        features: Lista de strings con los nombres de las carpetas en src/features/.
        
    Returns:
        List[str]: Nombres de las features que se registraron correctamente.
    """
    router = FeatureRouter(app)
    features_config = {name: True for name in features}
    return router.register_many(features_config)
