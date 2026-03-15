from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    TIMESTAMP,
    ForeignKey,
    UniqueConstraint,
    DateTime,
    func
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
    
    # Campos Profesionales
    batch_number = Column(String(50))
    expiry_date = Column(DateTime)
    purchase_date = Column(DateTime)
    supplier = Column(String(100))
    storage_location = Column(String(100))
    
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    apiary = relationship("ApiaryModel", back_populates="inventories")
    movements = relationship("InventoryMovementModel", back_populates="inventory", cascade="all, delete-orphan")

    __table_args__ = (UniqueConstraint("apiary_id", "name", name="uq_apiary_name"),)

class InventoryMovementModel(Base):
    __tablename__ = "inventory_movements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    inventory_id = Column(UUID(as_uuid=True), ForeignKey("inventory.id", ondelete="CASCADE"), nullable=False)
    movement_type = Column(String(20), nullable=False) # 'entry', 'exit', 'update', 'create', 'delete'
    quantity = Column(Integer, nullable=False)
    stock_before = Column(Integer, nullable=False)
    stock_after = Column(Integer, nullable=False)
    reason = Column(String(100))
    notes = Column(Text)
    date = Column(DateTime, default=datetime.utcnow)

    inventory = relationship("InventoryModel", back_populates="movements")
