import os
import uuid
from flask import Flask
from src.core.database.db import db, init_app
from src.features.questions.infrastructure.models.question_models import BaseQuestionModel

def seed_base_questions(app):
    questions_data = [
        {
            "question_id": "presencia_reina",
            "category": "Salud",
            "question": "¿Se observó a la reina",
            "type": "opciones",
            "is_required": True,
            "options": "Sí,No",
            "score": 10,
            "display_order": 1
        },
        {
            "question_id": "enfermedades",
            "category": "Salud",
            "question": "¿Signos de enfermedades (Loque, Varroa, etc.)",
            "type": "texto",
            "is_required": False,
            "score": 9, # Cambiado a entero según tu tabla
            "display_order": 2
        },
        {
            "question_id": "poblacion",
            "category": "Estado de la Colmena",
            "question": "Nivel de población",
            "type": "opciones",
            "is_required": True,
            "options": "Alta,Media,Baja",
            "score": 9,
            "display_order": 3
        },
        {
            "question_id": "cantidad_cria",
            "category": "Producción",
            "question": "Cantidad de cuadros de cría",
            "type": "numero",
            "is_required": True,
            "min_value": 0,
            "max_value": 20,
            "score": 8,
            "display_order": 4
        },
        {
            "question_id": "estado_general",
            "category": "Estado de la Colmena",
            "question": "¿Cuál es el estado general de la colmena",
            "type": "opciones",
            "is_required": True,
            "options": "Excelente,Bueno,Regular,Malo",
            "score": 8,
            "display_order": 5
        },
        {
            "question_id": "necesita_alimentacion",
            "category": "Alimentación",
            "question": "¿Necesita alimentación suplementaria",
            "type": "opciones",
            "is_required": True,
            "options": "Sí,No",
            "score": 7,
            "display_order": 6
        },
        {
            "question_id": "celdas_reales",
            "category": "Salud",
            "question": "¿Presencia de celdas reales",
            "type": "opciones",
            "is_required": True,
            "options": "Sí,No",
            "score": 7,
            "display_order": 7
        },
        {
            "question_id": "cantidad_miel",
            "category": "Producción",
            "question": "Cantidad de cuadros de miel",
            "type": "numero",
            "is_required": True,
            "min_value": 0,
            "max_value": 20,
            "score": 6,
            "display_order": 8
        },
        {
            "question_id": "espacio_disponible",
            "category": "Mantenimiento",
            "question": "¿Necesita más espacio (alzas)",
            "type": "opciones",
            "is_required": True,
            "options": "Sí,No",
            "score": 6,
            "display_order": 9
        },
        {
            "question_id": "comportamiento",
            "category": "Estado de la Colmena",
            "question": "Comportamiento de las abejas",
            "type": "opciones",
            "is_required": True,
            "options": "Dócil,Nervioso,Agresivo",
            "score": 5,
            "display_order": 10
        }
    ]

    with app.app_context():
        for data in questions_data:
            # Check by question_id
            existing = db.session.query(BaseQuestionModel).filter_by(question_id=data["question_id"]).first()
            if existing:
                print(f"Question '{data['question_id']}' already exists. Updating.")
                existing.category = data["category"]
                existing.question = data["question"]
                existing.type = data["type"]
                existing.is_required = data["is_required"]
                existing.options = data.get("options")
                existing.min_value = data.get("min_value")
                existing.max_value = data.get("max_value")
                existing.score = data.get("score")
                existing.display_order = data["display_order"]
            else:
                q = BaseQuestionModel(
                    id=uuid.uuid4(),
                    question_id=data["question_id"],
                    category=data["category"],
                    question=data["question"],
                    type=data["type"],
                    is_required=data["is_required"],
                    options=data.get("options"),
                    min_value=data.get("min_value"),
                    max_value=data.get("max_value"),
                    score=data.get("score"),
                    display_order=data["display_order"],
                    is_active=True
                )
                db.session.add(q)
        
        db.session.commit()
        print(f"Successfully seeded/updated base questions.")

if __name__ == "__main__":
    app = Flask(__name__)
    from dotenv import load_dotenv
    load_dotenv()
    
    class Config:
        DATABASE_URL = os.getenv('DATABASE_URL')
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        FRONTEND_URL = os.getenv('FRONTEND_URL', '')
        BASE_URL = os.getenv('BASE_URL', '')
        DEBUG = True
    
    app.config.from_object(Config)
    init_app(app)
    seed_base_questions(app)
