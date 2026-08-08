from uuid import UUID, uuid4
from src.features.questions.application.interfaces.repositories.question_repository import QuestionRepository
from src.features.questions.domain.entities.question import ApiaryQuestion
from src.features.questions.application.dto.question_dto import ApiaryQuestionDto
from src.features.questions.application.mappers.question_mapper import QuestionMapper

class CreateApiaryQuestion:
    def __init__(self, question_repository: QuestionRepository):
        self.question_repository = question_repository

    def execute(self, apiary_id: UUID, question_data: dict) -> ApiaryQuestionDto:
        # Extraer campos con soporte para alias del frontend
        question_text = question_data.get("question", question_data.get("question_text", "")).strip()
        
        # Validar signos de interrogación
        if question_text:
            if not question_text.startswith('¿'): question_text = f'¿{question_text}'
            if not question_text.endswith('?'): question_text = f'{question_text}?'

        question_type = question_data.get("type", question_data.get("question_type"))
        category = question_data.get("category", question_data.get("categoria", "General"))
        is_required = question_data.get("is_required", question_data.get("obligatoria", False))
        display_order = question_data.get("display_order", question_data.get("orden", 0))
        
        # Formatear opciones: asegurar que sea un string separado por comas sin basura
        options_raw = question_data.get("options", question_data.get("opciones"))
        options_str = None
        if isinstance(options_raw, list):
            options_str = ",".join([str(o).strip() for f in options_raw if (o := str(f).strip()) and o != '{}'])
        elif isinstance(options_raw, str):
            options_str = ",".join([o.strip() for f in options_raw.split(',') if (o := f.strip()) and o != '{}'])

        min_value = question_data.get("min_value", question_data.get("min"))
        max_value = question_data.get("max_value", question_data.get("max"))
        is_active = question_data.get("is_active", question_data.get("activa", True))

        new_apiary_q = ApiaryQuestion(
            id=uuid4(),
            apiary_id=apiary_id,
            question_id=question_data.get("question_id", f"custom_{uuid4().hex[:8]}"),
            category=category,
            question=question_text,
            type=question_type,
            display_order=display_order,
            is_required=is_required,
            options=options_str,
            min_value=min_value,
            max_value=max_value,
            depends_on=question_data.get("depends_on"),
            is_active=is_active,
            is_system=False, # Al ser creada por el usuario, no es de sistema
            score=question_data.get("score", 0)
        )
        
        entity = self.question_repository.create_apiary_question(new_apiary_q)
        return QuestionMapper.apiary_to_dto(entity)
