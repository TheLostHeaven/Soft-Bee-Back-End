from sqlalchemy import (
    Column,
    Integer,
    Text,
    TIMESTAMP,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from src.core.database.db import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.sql import func

class BeehiveModel(Base):
    __tablename__ = 'beehives'

    id = Column(UUID(), primary_key=True, default=uuid.uuid4, index=True)
    apiary_id = Column(UUID(), ForeignKey("apiaries.id", ondelete="CASCADE"), nullable=False)
    activity_level = Column(Text, nullable=True)
    bee_population = Column(Text, nullable=True)
    food_frames = Column(Integer)
    brood_frames = Column(Integer)
    hive_status = Column(Text, nullable=True)
    health_status = Column(Text, nullable=True)
    has_production_chamber = Column(Text, nullable=True)
    observations = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    apiary = relationship("ApiaryModel", back_populates="hives")

    def __repr__(self):
        return f'<BeehiveModel {self.id}>'