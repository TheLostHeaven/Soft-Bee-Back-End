from sqlalchemy import (
    Column,
    Integer,
    Text,
    TIMESTAMP,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from src.core.database.db import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

class BeehiveModel(db.Model):
    __tablename__ = 'beehives'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    apiary_id = Column(UUID(as_uuid=True), ForeignKey("apiaries.id", ondelete="CASCADE"), nullable=False)
    activity_level = Column(Text, nullable=True)
    bee_population = Column(Text, nullable=True)
    food_frames = Column(Integer)
    brood_frames = Column(Integer)
    hive_status = Column(Text, nullable=True)
    health_status = Column(Text, nullable=True)
    has_production_chamber = Column(Text, nullable=True)
    observations = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint('apiary_id', 'beehive_number', name='_apiary_beehive_number_uc'),
    )

    def __repr__(self):
        return f'<BeehiveModel {self.beehive_id}>'