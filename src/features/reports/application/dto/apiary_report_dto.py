from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from datetime import datetime


class ApiaryInfoDto(BaseModel):
    """DTO para información básica del apiario"""
    id: UUID
    user_id: UUID
    name: str
    location: Optional[str]
    beehives_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BeehiveInfoDto(BaseModel):
    """DTO para información de colmena"""
    id: UUID
    hive_number: int
    activity_level: Optional[str]
    bee_population: Optional[str]
    food_frames: Optional[int]
    brood_frames: Optional[int]
    hive_status: Optional[str]
    health_status: Optional[str]
    has_production_chamber: Optional[str]
    observations: Optional[str]
    treatments: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class InventoryInfoDto(BaseModel):
    """DTO para información de inventario"""
    id: UUID
    name: str
    quantity: int
    unit: str
    description: Optional[str]
    minimum_stock: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class QuestionAnswerInfoDto(BaseModel):
    """DTO para pregunta y respuesta"""
    question_id: str
    category: str
    question: str
    answer: Optional[str]
    score: int
    answered_at: Optional[datetime]

    class Config:
        from_attributes = True


class BeehiveDetailReportDto(BaseModel):
    """DTO para reporte detallado de colmena"""
    beehive: BeehiveInfoDto
    questions_answers: List[QuestionAnswerInfoDto]

    class Config:
        from_attributes = True


class ApiaryReportDto(BaseModel):
    """DTO para reporte completo del apiario"""
    apiary: ApiaryInfoDto
    inventory: List[InventoryInfoDto]
    beehives: List[BeehiveDetailReportDto]
    total_questions: int
    total_answers: int
    generated_at: datetime

    class Config:
        from_attributes = True
