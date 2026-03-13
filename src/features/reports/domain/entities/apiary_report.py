from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from uuid import UUID


@dataclass
class ApiaryInfo:
    """Información básica del apiario"""
    id: UUID
    user_id: UUID
    name: str
    location: Optional[str]
    beehives_count: int
    created_at: datetime
    updated_at: datetime


@dataclass
class BeehiveInfo:
    """Información de una colmena"""
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


@dataclass
class InventoryInfo:
    """Información de inventario"""
    id: UUID
    name: str
    quantity: int
    unit: str
    description: Optional[str]
    minimum_stock: int
    created_at: datetime
    updated_at: datetime


@dataclass
class QuestionAnswerInfo:
    """Información de pregunta y respuesta"""
    question_id: str
    category: str
    question: str
    answer: Optional[str]
    score: int
    answered_at: Optional[datetime]


@dataclass
class BeehiveDetailReport:
    """Reporte detallado de una colmena"""
    beehive: BeehiveInfo
    questions_answers: List[QuestionAnswerInfo]


@dataclass
class ApiaryReport:
    """Reporte completo del apiario"""
    apiary: ApiaryInfo
    inventory: List[InventoryInfo]
    beehives: List[BeehiveDetailReport]
    total_questions: int
    total_answers: int
    generated_at: datetime
