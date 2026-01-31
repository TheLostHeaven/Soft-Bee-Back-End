from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from src.features.beehive.domain.enums.beehive_enums import ActivityLevel, BeePopulation, HiveStatus, HealthStatus, HasProductionChamber

class CreateBeehiveRequestSchema(BaseModel):
    apiary_id: UUID = Field(..., example="2142ebd4-1311-4ea1-95d4-710dd8e69ae0")
    beehive_number: int = Field(..., example=101)
    activity_level: ActivityLevel = Field(..., example=ActivityLevel.Alta)
    bee_population: BeePopulation = Field(..., example=BeePopulation.Media)
    food_frames: int = Field(..., example=5)
    brood_frames: int = Field(..., example=3)
    hive_status: HiveStatus = Field(..., example=HiveStatus.CamaraDeCriaYProduccion)
    health_status: HealthStatus = Field(..., example=HealthStatus.Ninguno)
    has_production_chamber: HasProductionChamber = Field(..., example=HasProductionChamber.Si)
    observations: Optional[str] = Field(None, example="La colmena se ve saludable.")

class UpdateBeehiveRequestSchema(BaseModel):
    activity_level: Optional[ActivityLevel] = Field(None, example=ActivityLevel.Media)
    bee_population: Optional[BeePopulation] = Field(None, example=BeePopulation.Alta)
    food_frames: Optional[int] = Field(None, example=6)
    brood_frames: Optional[int] = Field(None, example=4)
    hive_status: Optional[HiveStatus] = Field(None, example=HiveStatus.CamaraDeCriaYDobleAlzaDeProduccion)
    health_status: Optional[HealthStatus] = Field(None, example=HealthStatus.PresenciaBarroa)
    has_production_chamber: Optional[HasProductionChamber] = Field(None, example=HasProductionChamber.No)
    observations: Optional[str] = Field(None, example="Se observó presencia de varroa.")

class BeehiveResponseSchema(BaseModel):
    id: UUID = Field(..., alias="beehive_id")
    apiary_id: UUID
    beehive_number: int
    activity_level: str
    bee_population: str
    food_frames: int
    brood_frames: int
    hive_status: str
    health_status: str
    has_production_chamber: str
    observations: Optional[str]
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True
