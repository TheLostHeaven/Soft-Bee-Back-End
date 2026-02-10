from typing import Optional, Union
from pydantic import BaseModel, Field
from uuid import UUID


class CreateBeehiveDTO(BaseModel):
    apiary_id: UUID = Field(..., example="2142ebd4-1311-4ea1-95d4-4242ebd4-1311-4ea1-95d4-710dd8e69ae0")
    beehive_number: int = Field(..., example=101)
    activity_level: Optional[str] = Field(default=None)
    bee_population: Optional[str] = Field(default=None)
    food_frames: Optional[int] = Field(default=None)
    brood_frames: Optional[int] = Field(default=None)
    hive_status: Optional[str] = Field(default=None)
    health_status: Optional[str] = Field(default=None)
    has_production_chamber: Optional[str] = Field(default=None)
    observations: Optional[str] = Field(default=None)


class UpdateBeehiveDTO(BaseModel):
    activity_level: Optional[str] = Field(None, example="Media")
    bee_population: Optional[str] = Field(None, example="Alta")
    food_frames: Optional[int] = Field(None, example=6)
    brood_frames: Optional[int] = Field(None, example=4)
    hive_status: Optional[str] = Field(None, example="Cámara de cría y doble alza de producción")
    health_status: Optional[str] = Field(None, example="Presencia barroa")
    has_production_chamber: Optional[str] = Field(None, example="No")
    observations: Optional[str] = Field(None, example="Se observó presencia de varroa.")


class BeehiveDTO(BaseModel):
    beehive_id: UUID
    apiary_id: UUID
    beehive_number: int
    activity_level: Optional[str]
    bee_population: Optional[str]
    food_frames: Optional[int]
    brood_frames: Optional[int]
    hive_status: Optional[str]
    health_status: Optional[str]
    has_production_chamber: Optional[str]
    observations: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        from_attributes = True
