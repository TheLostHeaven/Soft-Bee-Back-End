from enum import Enum

class ActivityLevel(str, Enum):
    ALTA = "Alta"
    MEDIA = "Media"
    BAJA = "Baja"

class BeePopulation(str, Enum):
    ALTA = "Alta"
    MEDIA = "Media"
    BAJA = "Baja"

class HiveStatus(str, Enum):
    CAMARA_CRIA_PRODUCCION = "Cámara de cría y producción"
    CAMARA_CRIA_DOBLE_ALZA = "Cámara de cría y doble alza de producción"
    CAMARA_CRIA = "Cámara de cría"
    CAMARA_PRODUCCION = "Cámara de producción"

class HealthStatus(str, Enum):
    NINGUNO = "Ninguno"
    PRESENCIA_BARROA = "Presencia barroa"
    PRESENCIA_POLILLA = "Presencia de polilla"
    PRESENCIA_CURRUNCHO = "Presencia de curruncho"
    MORTALIDAD_MALFORMACION = "Mortalidad- malformación en nodrizas"

class HasProductionChamber(str, Enum):
    SI = "Si"
    NO = "No"