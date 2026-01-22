from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from src.core.database.db import Base
from src.features.auth.infrastructure.models.user_model import UserModel # Import UserModel

class ApiaryModel(Base):
    """SQLAlchemy model for apiaries"""
    __tablename__ = "apiaries"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False) # Define as foreign key
    name = Column(String(100), nullable=False)
    location = Column(String(50), nullable=True)
    beehives_count = Column(Integer, default=0)
    treatments = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Define relationship to User
    beekeeper = relationship("UserModel", backref="apiaries")
    
    def __repr__(self):
        return f"<Apiary(id={self.id}, name={self.name}, user_id={self.user_id}, beehives_count={self.beehives_count})>"
