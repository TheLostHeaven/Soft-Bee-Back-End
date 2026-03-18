from pydantic import BaseModel
from typing import List, Dict, Any
from uuid import UUID
from datetime import datetime

class ApiaryStatisticsSchema(BaseModel):
    apiary_id: UUID
    total_beehives: int
    active_treatments: int
    avg_health_score: float
    total_inventory_items: int
    low_stock_items: int
    last_updated: datetime
    
    class Config:
        from_attributes = True

class BeehiveHealthTrendSchema(BaseModel):
    hive_id: UUID
    hive_number: int
    data_points: List[Dict[str, Any]]
    
    class Config:
        from_attributes = True

class TreatmentDistributionSchema(BaseModel):
    treatment_type: str
    count: int
    percentage: float
    
    class Config:
        from_attributes = True

class InventoryLevelSchema(BaseModel):
    item_name: str
    current_quantity: int
    minimum_stock: int
    status: str
    
    class Config:
        from_attributes = True

class AnswerScoreTrendSchema(BaseModel):
    category: str
    data_points: List[Dict[str, Any]]
    
    class Config:
        from_attributes = True
