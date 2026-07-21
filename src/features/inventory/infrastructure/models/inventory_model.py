from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    TIMESTAMP,
    ForeignKey,
    UniqueConstraint,
    DateTime
)
from datetime import datetime
from sqlalchemy.orm import relationship
from src.core.database.db import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid

class InventoryModel(Base):
    __tablename__ = "inventory"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    apiary_id = Column(UUID(as_uuid=True), ForeignKey("apiaries.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False, default="General")
    quantity = Column(Integer, nullable=False, default=0)
    unit = Column(String(50), nullable=False, default="unit")
    description = Column(Text)
    minimum_stock = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    apiary = relationship("ApiaryModel", back_populates="inventories")

    __table_args__ = (UniqueConstraint("apiary_id", "name", name="uq_apiary_name"),)
