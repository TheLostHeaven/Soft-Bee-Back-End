from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from src.features.beehive.domain.enums.beehive_enums import ActivityLevel, BeePopulation, HiveStatus, HealthStatus, HasProductionChamber

class CreateBeehiveRequestSchema(BaseModel):
    apiary_id: UUID = Field(..., example="2142ebd4-1311-4ea1-95d4-710dd8e69ae0")
    beehive_number: Optional[int] = Field(None, example=101)
    activity_level: Optional[ActivityLevel] = Field(None, example=ActivityLevel.Alta)
    bee_population: Optional[BeePopulation] = Field(None, example=BeePopulation.Media)
    food_frames: Optional[int] = Field(None, example=5)
    brood_frames: Optional[int] = Field(None, example=3)
    hive_status: Optional[HiveStatus] = Field(None, example=HiveStatus.CamaraDeCriaYProduccion)
    health_status: Optional[HealthStatus] = Field(None, example=HealthStatus.Ninguno)
    has_production_chamber: Optional[HasProductionChamber] = Field(None, example=HasProductionChamber.Si)
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
    beehive_number: Optional[int]
    activity_level: Optional[str]
    bee_population: Optional[str]
    food_frames: Optional[int]
    brood_frames: Optional[int]
    hive_status: Optional[str]
    health_status: Optional[str]
    has_production_chamber: Optional[str]
    observations: Optional[str]
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True
