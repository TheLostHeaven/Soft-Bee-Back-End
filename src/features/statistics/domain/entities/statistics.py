from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime
from uuid import UUID

@dataclass
class ApiaryStatistics:
    """Estadísticas generales de un apiario"""
    apiary_id: UUID
    total_beehives: int
    active_treatments: int
    avg_health_score: float
    total_inventory_items: int
    low_stock_items: int
    last_updated: datetime

@dataclass
class BeehiveHealthTrend:
    """Tendencia de salud de colmenas"""
    hive_id: UUID
    hive_number: int
    data_points: List[Dict[str, Any]]  # [{date, score, status}]

@dataclass
class TreatmentDistribution:
    """Distribución de tratamientos"""
    treatment_type: str
    count: int
    percentage: float

@dataclass
class InventoryLevel:
    """Niveles de inventario"""
    item_name: str
    current_quantity: int
    minimum_stock: int
    status: str  # 'ok', 'low', 'critical'

@dataclass
class AnswerScoreTrend:
    """Tendencia de scores de respuestas"""
    category: str
    data_points: List[Dict[str, Any]]  # [{date, avg_score, count}]
