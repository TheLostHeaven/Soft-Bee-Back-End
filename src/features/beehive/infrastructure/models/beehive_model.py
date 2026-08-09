from sqlalchemy import (
    Column,
    Integer,
    Text,
    TIMESTAMP,
    ForeignKey,
    Boolean,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from src.core.database.db import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.sql import func

class BeehiveModel(Base):
    __tablename__ = 'beehives'
    __table_args__ = (
        UniqueConstraint('apiary_id', 'hive_number', name='uq_apiary_hive_number'),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    apiary_id = Column(UUID(as_uuid=True), ForeignKey("apiaries.id", ondelete="CASCADE"), nullable=False)
    hive_number = Column(Integer, nullable=False)
    activity_level = Column(Text, nullable=True)
    bee_population = Column(Text, nullable=True)
    food_frames = Column(Integer)
    brood_frames = Column(Integer)
    hive_status = Column(Text, nullable=True)
    health_status = Column(Text, nullable=True)
    has_production_chamber = Column(Text, nullable=True)
    observations = Column(Text)
    treatments = Column(Boolean, default=False, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    apiary = relationship("ApiaryModel", back_populates="hives")

    def __repr__(self):
        return f'<BeehiveModel {self.id}>'
