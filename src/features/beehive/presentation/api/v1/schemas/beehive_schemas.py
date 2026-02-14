from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

class CreateBeehiveRequestSchema(BaseModel):
    apiary_id: UUID = Field(..., example="2142ebd4-1311-4ea1-95d4-710dd8e69ae0")
    activity_level: Optional[str] = Field(None, example="Alta")
    bee_population: Optional[str] = Field(None, example="Media")
    food_frames: Optional[int] = Field(None, example=5)
    brood_frames: Optional[int] = Field(None, example=3)
    hive_status: Optional[str] = Field(None, example="Camara de cria y produccion")
    health_status: Optional[str] = Field(None, example="Ninguno")
    has_production_chamber: Optional[str] = Field(None, example="Si")
    observations: Optional[str] = Field(None, example="La colmena se ve saludable.")

class UpdateBeehiveRequestSchema(BaseModel):
    activity_level: Optional[str] = Field(None, example="Media")
    bee_population: Optional[str] = Field(None, example="Alta")
    food_frames: Optional[int] = Field(None, example=6)
    brood_frames: Optional[int] = Field(None, example=4)
    hive_status: Optional[str] = Field(None, example="Camara de cria y produccion")
    health_status: Optional[str] = Field(None, example="Presencia de varroa")
    has_production_chamber: Optional[str] = Field(None, example="No")
    observations: Optional[str] = Field(None, example="Se observó presencia de varroa.")

class BeehiveResponseSchema(BaseModel):
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
