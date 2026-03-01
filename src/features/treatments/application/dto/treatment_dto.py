from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional, List
from uuid import UUID

class CreateFollowupDTO(BaseModel):
    treatment_id: UUID
    review_date: date
    hive_condition: Optional[str] = None
    observed_changes: Optional[str] = None
    partial_results: Optional[str] = None
    infestation_level: Optional[str] = None
    notes: Optional[str] = None
    reviewer: Optional[str] = None

class FollowupDTO(BaseModel):
    followup_id: UUID
    treatment_id: UUID
    review_date: date
    hive_condition: Optional[str] = None
    observed_changes: Optional[str] = None
    partial_results: Optional[str] = None
    infestation_level: Optional[str] = None
    notes: Optional[str] = None
    reviewer: Optional[str] = None
    registration_date: Optional[datetime] = None

class CreateTreatmentDTO(BaseModel):
    hive_id: UUID
    treatment_type: str
    product_name: str
    start_date: date
    active_ingredient: Optional[str] = None
    target_disease: Optional[str] = None
    estimated_duration_days: Optional[int] = None
    end_date: Optional[date] = None
    application_method: Optional[str] = None
    dosage_applied: Optional[str] = None
    dosage_unit: Optional[str] = None
    batch_number: Optional[str] = None
    supplier: Optional[str] = None
    expiry_date: Optional[date] = None
    applied_by: Optional[str] = None

class TreatmentDTO(BaseModel):
    id: UUID
    hive_id: UUID
    treatment_type: str
    product_name: str
    start_date: date
    active_ingredient: Optional[str] = None
    target_disease: Optional[str] = None
    estimated_duration_days: Optional[int] = None
    end_date: Optional[date] = None
    application_method: Optional[str] = None
    dosage_applied: Optional[str] = None
    dosage_unit: Optional[str] = None
    batch_number: Optional[str] = None
    supplier: Optional[str] = None
    expiry_date: Optional[date] = None
    status: str
    final_result: Optional[str] = None
    final_hive_condition: Optional[str] = None
    requires_repeat: bool
    future_recommendations: Optional[str] = None
    applied_by: Optional[str] = None
    registration_date: Optional[datetime] = None
    update_date: Optional[datetime] = None
    followups: List[FollowupDTO] = []
