from typing import Optional, Union
from pydantic import BaseModel, Field
from uuid import UUID


class CreateBeehiveDTO(BaseModel):
    apiary_id: UUID
    activity_level: Optional[str] = Field(None, example="Bajo")
    bee_population: Optional[str] = Field(None, example="Media")
    food_frames: Optional[int] = Field(None, example=5)
    brood_frames: Optional[int] = Field(None, example=3)
    hive_status: Optional[str] = Field(None, example="Activa")
    health_status: Optional[str] = Field(None, example="Saludable")
    has_production_chamber: Optional[str] = Field(None, example="No")
    observations: Optional[str] = Field(None, example="Sin observaciones.")


class UpdateBeehiveDTO(BaseModel):
    activity_level: Optional[str] = Field(None, example="Media")
    bee_population: Optional[str] = Field(None, example="Alta")
    food_frames: Optional[int] = Field(None, example=6)
    brood_frames: Optional[int] = Field(None, example=4)
    hive_status: Optional[str] = Field(None, example="Camara de cria y produccion")
    health_status: Optional[str] = Field(None, example="Presencia de varroa")
    has_production_chamber: Optional[str] = Field(None, example="No")
    observations: Optional[str] = Field(None, example="Se observó presencia de varroa.")


class BeehiveDTO(BaseModel):
    id: UUID
    apiary_id: UUID
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
