from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Index, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from src.core.database.db import Base

class HiveAnswerModel(Base):
    """SQLAlchemy model for hive answers with full history tracking"""
    __tablename__ = "hive_answers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hive_question_id = Column(UUID(as_uuid=True), ForeignKey('hive_questions.id', ondelete='CASCADE'), nullable=False)
    answer = Column(Text, nullable=True)  # Cambiado de answer_value a answer para coincidir con tu estructura
    score = Column(Integer, default=0)
    answered_by = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    answered_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    hive_question = relationship("HiveQuestionModel")
    user = relationship("UserModel", foreign_keys=[answered_by])

    # Indexes for performance
    __table_args__ = (
        Index('idx_answers_hive_question_id', 'hive_question_id'),
        Index('idx_answers_answered_by', 'answered_by'),
        Index('idx_answers_answered_at', 'answered_at'),
        Index('idx_answers_hive_question_date', 'hive_question_id', 'answered_at'),
    )

    def __repr__(self):
        return f"<HiveAnswer(id={self.id}, hive_question_id={self.hive_question_id}, answer={self.answer[:20] if self.answer else None})>"
