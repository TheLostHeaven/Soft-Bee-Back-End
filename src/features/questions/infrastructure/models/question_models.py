from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Boolean, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from src.core.database.db import Base

class ApiaryQuestionModel(Base):
    """SQLAlchemy model for apiary-specific questions"""
    __tablename__ = "apiary_questions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    apiary_id = Column(UUID(as_uuid=True), ForeignKey('apiaries.id', ondelete='CASCADE'), nullable=False)
    question_id = Column(String(50), nullable=False) # Identificador lógico (ej: presencia_reina)
    
    category = Column(String(100), nullable=False)
    question = Column(String(100), nullable=False)
    type = Column(String(100), nullable=False)
    is_required = Column(Boolean, nullable=False, default=False)
    options = Column(String(100))
    display_order = Column(Integer, nullable=False)
    min_value = Column(Integer)
    max_value = Column(Integer)
    depends_on = Column(Text)
    score = Column(Integer, default=0)
    is_active = Column(Boolean, nullable=False, default=True)
    is_system = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (UniqueConstraint('apiary_id', 'question_id', name='_apiary_question_uc'),)

    def __repr__(self):
        return f"<ApiaryQuestion(id={self.id}, question_id={self.question_id})>"

class HiveQuestionModel(Base):
    """SQLAlchemy model for hive-specific questions"""
    __tablename__ = "hive_questions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hive_id = Column(UUID(as_uuid=True), ForeignKey('beehives.id', ondelete='CASCADE'), nullable=False)
    apiary_question_id = Column(UUID(as_uuid=True), ForeignKey('apiary_questions.id', ondelete='CASCADE'), nullable=False)
    display_order = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    assigned_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    apiary_question = relationship("ApiaryQuestionModel")
    
    __table_args__ = (UniqueConstraint('hive_id', 'apiary_question_id', name='_hive_question_uc'),)

    def __repr__(self):
        return f"<HiveQuestion(id={self.id}, hive_id={self.hive_id}, apiary_question_id={self.apiary_question_id})>"
