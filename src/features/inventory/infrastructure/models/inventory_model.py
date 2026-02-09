from src.core.database.db import db, Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UUID
from sqlalchemy.orm import relationship
from datetime import datetime


class InventoryModel(db.Model):
    __tablename__ = 'inventory'

    id = Column(UUID(as_uuid=True), primary_key=True, default=db.text("gen_random_uuid()"))
    apiary_id = Column(UUID(as_uuid=True), ForeignKey('apiaries.id'), nullable=False)
    name = Column(String(100), nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    unit = Column(String(50), nullable=False)
    description = Column(String(255), nullable=True)
    minimum_stock = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relación con el modelo de Apiario (asumiendo que existe un modelo ApiaryModel)
    apiary = relationship("ApiaryModel", backref="inventory_items")

    def __repr__(self):
        return f"<InventoryModel(id='{self.id}', name='{self.name}', apiary_id='{self.apiary_id}')>"

    def to_dict(self):
        return {
            'id': str(self.id),
            'apiary_id': str(self.apiary_id),
            'name': self.name,
            'quantity': self.quantity,
            'unit': self.unit,
            'description': self.description,
            'minimum_stock': self.minimum_stock,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    @staticmethod
    def from_dict(data: dict):
        return InventoryModel(
            id=data.get('id'),
            apiary_id=data.get('apiary_id'),
            name=data.get('name'),
            quantity=data.get('quantity'),
            unit=data.get('unit'),
            description=data.get('description'),
            minimum_stock=data.get('minimum_stock'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )