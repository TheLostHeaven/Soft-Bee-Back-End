from enum import Enum

class ActivityLevel(Enum):
    Alta = "Alta"
    Media = "Media"
    Baja = "Baja"

class BeePopulation(Enum):
    Alta = "Alta"
    Media = "Media"
    Baja = "Baja"

class HiveStatus(Enum):
    CamaraDeCriaYProduccion = "Cámara de cría y producción"
    CamaraDeCriaYDobleAlzaDeProduccion = "Cámara de cría y doble alza de producción"
    CamaraDeCria = "Cámara de cría"
    CamaraDeProduccion = "Cámara de producción"

class HealthStatus(Enum):
    Ninguno = "Ninguno"
    PresenciaBarroa = "Presencia barroa"
    PresenciaDePlagas = "Presencia de plagas"
    Enfermedad = "Enfermedad"

class HasProductionChamber(Enum):
    Si = "Si"
    No = "No"
