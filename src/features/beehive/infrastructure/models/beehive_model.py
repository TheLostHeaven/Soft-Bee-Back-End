import uuid
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from src.core.database.db import db
from sqlalchemy.orm import relationship

class BeehiveModel(db.Model):
    __tablename__ = 'beehives'

    beehive_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    apiary_id = Column(UUID(as_uuid=True), ForeignKey('apiaries.id', ondelete='CASCADE'), nullable=False)
    beehive_number = Column(Integer, nullable=False)
    activity_level = Column(Text)
    bee_population = Column(Text)
    food_frames = Column(Integer)
    brood_frames = Column(Integer)
    hive_status = Column(Text)
    health_status = Column(Text)
    has_production_chamber = Column(Text)
    observations = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    apiary = relationship("ApiaryModel", back_populates="hives")

    __table_args__ = (
        UniqueConstraint('apiary_id', 'beehive_number', name='_apiary_beehive_number_uc'),
    )

    def __repr__(self):
        return f'<BeehiveModel {self.beehive_id}>'