from typing import Optional, Union
from pydantic import BaseModel, Field
from uuid import UUID
from src.features.beehive.domain.enums.beehive_enums import ActivityLevel, BeePopulation, HiveStatus, HealthStatus, HasProductionChamber


class CreateBeehiveDTO(BaseModel):
    apiary_id: UUID = Field(..., example="2142ebd4-1311-4ea1-95d4-710dd8e69ae0")
    beehive_number: int = Field(..., example=101)
    activity_level: Optional[ActivityLevel] = Field(default=None)
    bee_population: Optional[BeePopulation] = Field(default=None)
    food_frames: Optional[int] = Field(default=None)
    brood_frames: Optional[int] = Field(default=None)
    hive_status: Optional[HiveStatus] = Field(default=None)
    health_status: Optional[HealthStatus] = Field(default=None)
    has_production_chamber: Optional[HasProductionChamber] = Field(default=None)
    observations: Optional[str] = Field(default=None)


class UpdateBeehiveDTO(BaseModel):
    activity_level: Optional[ActivityLevel] = Field(None, example=ActivityLevel.Media)
    bee_population: Optional[BeePopulation] = Field(None, example=BeePopulation.Alta)
    food_frames: Optional[int] = Field(None, example=6)
    brood_frames: Optional[int] = Field(None, example=4)
    hive_status: Optional[HiveStatus] = Field(None, example=HiveStatus.CamaraDeCriaYDobleAlzaDeProduccion)
    health_status: Optional[HealthStatus] = Field(None, example=HealthStatus.PresenciaBarroa)
    has_production_chamber: Optional[HasProductionChamber] = Field(None, example=HasProductionChamber.No)
    observations: Optional[str] = Field(None, example="Se observó presencia de varroa.")


class BeehiveDTO(BaseModel):
    beehive_id: UUID
    apiary_id: UUID
    beehive_number: int
    activity_level: Optional[ActivityLevel]
    bee_population: Optional[BeePopulation]
    food_frames: Optional[int]
    brood_frames: Optional[int]
    hive_status: Optional[HiveStatus]
    health_status: Optional[HealthStatus]
    has_production_chamber: Optional[HasProductionChamber]
    observations: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        from_attributes = True
