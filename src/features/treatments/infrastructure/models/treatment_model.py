from sqlalchemy import Column, Integer, String, Text, Date, Boolean, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from src.core.database.db import Base

class TreatmentModel(Base):
    __tablename__ = 'treatments'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hive_id = Column(UUID(as_uuid=True), ForeignKey('beehives.id', ondelete='CASCADE'), nullable=False)
    treatment_type = Column(String(50), nullable=False)
    product_name = Column(String(100), nullable=False)
    active_ingredient = Column(String(100))
    target_disease = Column(String(100))
    start_date = Column(Date, nullable=False)
    estimated_duration_days = Column(Integer)
    end_date = Column(Date)
    application_method = Column(String(50))
    dosage_applied = Column(String(50))
    dosage_unit = Column(String(20))
    batch_number = Column(String(50))
    supplier = Column(String(100))
    expiry_date = Column(Date)
    status = Column(String(20), default='active')
    final_result = Column(String(20))
    final_hive_condition = Column(Text)
    requires_repeat = Column(Boolean, default=False)
    future_recommendations = Column(Text)
    applied_by = Column(String(100))
    registration_date = Column(TIMESTAMP, server_default=func.now())
    update_date = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    # Relationship with followups
    followups = relationship("TreatmentFollowupModel", back_populates="treatment", cascade="all, delete-orphan")
    # hive = relationship("BeehiveModel", back_populates="treatments") # If BeehiveModel has treatments relationship

    def __repr__(self):
        return f'<TreatmentModel {self.id}>'

class TreatmentFollowupModel(Base):
    __tablename__ = 'treatment_followups'

    followup_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    treatment_id = Column(UUID(as_uuid=True), ForeignKey('treatments.id', ondelete='CASCADE'), nullable=False)
    review_date = Column(Date, nullable=False)
    hive_condition = Column(String(50))
    observed_changes = Column(Text)
    partial_results = Column(Text)
    infestation_level = Column(String(20))
    notes = Column(Text)
    reviewer = Column(String(100))
    registration_date = Column(TIMESTAMP, server_default=func.now())

    treatment = relationship("TreatmentModel", back_populates="followups")

    def __repr__(self):
        return f'<TreatmentFollowupModel {self.followup_id}>'
