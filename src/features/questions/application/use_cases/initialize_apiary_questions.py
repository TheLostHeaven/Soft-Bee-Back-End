from uuid import uuid4, UUID
from typing import List
from src.features.questions.application.interfaces.repositories.question_repository import QuestionRepository
from src.features.questions.domain.entities.question import ApiaryQuestion

class InitializeApiaryQuestions:
    def __init__(self, question_repository: QuestionRepository):
        self.question_repository = question_repository

    def execute(self, apiary_id: UUID) -> List[ApiaryQuestion]:
        # Banco de preguntas base definido directamente en el código
        base_questions_data = [
            {
                "question_id": "presencia_reina",
                "category": "Salud",
                "question": "¿Se observó a la reina?",
                "type": "opciones",
                "is_required": True,
                "options": "Sí,No",
                "score": 10,
                "display_order": 1
            },
            {
                "question_id": "enfermedades",
                "category": "Salud",
                "question": "¿Signos de enfermedades (Loque, Varroa, etc.)?",
                "type": "texto",
                "is_required": False,
                "score": 9,
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
                "question": "¿Cuál es el estado general de la colmena?",
                "type": "opciones",
                "is_required": True,
                "options": "Excelente,Bueno,Regular,Malo",
                "score": 8,
                "display_order": 5
            },
            {
                "question_id": "necesita_alimentacion",
                "category": "Alimentación",
                "question": "¿Necesita alimentación suplementaria?",
                "type": "opciones",
                "is_required": True,
                "options": "Sí,No",
                "score": 7,
                "display_order": 6
            },
            {
                "question_id": "celdas_reales",
                "category": "Salud",
                "question": "¿Presencia de celdas reales?",
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
                "question": "¿Necesita más espacio (alzas)?",
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
        
        apiary_questions = []
        for data in base_questions_data:
            aq = ApiaryQuestion(
                id=uuid4(),
                apiary_id=apiary_id,
                question_id=data["question_id"],
                category=data["category"],
                question=data["question"],
                type=data["type"],
                display_order=data["display_order"],
                is_required=data["is_required"],
                options=data.get("options"),
                min_value=data.get("min_value"),
                max_value=data.get("max_value"),
                is_active=True,
                is_system=True,
                score=data["score"]
            )
            apiary_questions.append(aq)
            
        return self.question_repository.create_apiary_questions_batch(apiary_questions)
