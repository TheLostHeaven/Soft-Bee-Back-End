from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from src.core.database.db import Base

class QuestionModel(Base):
    """SQLAlchemy model for questions"""
    __tablename__ = "questions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    apiary_id = Column(UUID(as_uuid=True), ForeignKey('apiaries.id', ondelete='CASCADE'), nullable=False)
    external_id = Column(String(255), nullable=True)
    question_text = Column(String, nullable=False)
    question_type = Column(String(50), nullable=False) # e.g., 'texto', 'numero', 'opciones', 'rango'
    category = Column(String(100), nullable=True)
    is_required = Column(Boolean, default=False, nullable=False)
    display_order = Column(Integer, default=0, nullable=False)
    min_value = Column(Integer, nullable=True)
    max_value = Column(Integer, nullable=True)
    options = Column(JSONB, nullable=True)
    depends_on = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Question(id={self.id}, text='{self.question_text[:20]}...', type={self.question_type})>"
