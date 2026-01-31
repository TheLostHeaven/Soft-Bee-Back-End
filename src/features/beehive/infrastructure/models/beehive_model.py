from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    TIMESTAMP,
    ForeignKey,
    Enum
)
from sqlalchemy.orm import relationship
from src.core.database.db import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.sql import func
from src.features.beehive.domain.enums.beehive_enums import ActivityLevel, BeePopulation, HiveStatus, HealthStatus, HasProductionChamber


class BeehiveModel(Base):
    __tablename__ = "beehives"

    beehive_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    apiary_id = Column(UUID(as_uuid=True), ForeignKey("apiaries.id", ondelete="CASCADE"), nullable=False)
    beehive_number = Column(Integer, nullable=False)
    activity_level = Column(Enum(ActivityLevel), nullable=False)
    bee_population = Column(Enum(BeePopulation), nullable=False)
    food_frames = Column(Integer)
    brood_frames = Column(Integer)
    hive_status = Column(Enum(HiveStatus), nullable=False)
    health_status = Column(Enum(HealthStatus), nullable=False)
    has_production_chamber = Column(Enum(HasProductionChamber), nullable=False)
    observations = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    apiary = relationship("ApiaryModel", back_populates="hives")
