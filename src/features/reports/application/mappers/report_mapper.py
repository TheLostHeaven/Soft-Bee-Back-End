from src.features.reports.domain.entities.apiary_report import (
    ApiaryReport,
    ApiaryInfo,
    BeehiveInfo,
    InventoryInfo,
    QuestionAnswerInfo,
    BeehiveDetailReport
)
from src.features.reports.application.dto.apiary_report_dto import (
    ApiaryReportDto,
    ApiaryInfoDto,
    BeehiveInfoDto,
    InventoryInfoDto,
    QuestionAnswerInfoDto,
    BeehiveDetailReportDto
)


class ReportMapper:
    """Mapper para convertir entidades de reporte a DTOs"""

    @staticmethod
    def apiary_info_to_dto(entity: ApiaryInfo) -> ApiaryInfoDto:
        return ApiaryInfoDto(
            id=entity.id,
            user_id=entity.user_id,
            name=entity.name,
            location=entity.location,
            beehives_count=entity.beehives_count,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    @staticmethod
    def beehive_info_to_dto(entity: BeehiveInfo) -> BeehiveInfoDto:
        return BeehiveInfoDto(
            id=entity.id,
            hive_number=entity.hive_number,
            activity_level=entity.activity_level,
            bee_population=entity.bee_population,
            food_frames=entity.food_frames,
            brood_frames=entity.brood_frames,
            hive_status=entity.hive_status,
            health_status=entity.health_status,
            has_production_chamber=entity.has_production_chamber,
            observations=entity.observations,
            treatments=entity.treatments,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    @staticmethod
    def inventory_info_to_dto(entity: InventoryInfo) -> InventoryInfoDto:
        return InventoryInfoDto(
            id=entity.id,
            name=entity.name,
            quantity=entity.quantity,
            unit=entity.unit,
            description=entity.description,
            minimum_stock=entity.minimum_stock,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    @staticmethod
    def question_answer_to_dto(entity: QuestionAnswerInfo) -> QuestionAnswerInfoDto:
        return QuestionAnswerInfoDto(
            question_id=entity.question_id,
            category=entity.category,
            question=entity.question,
            answer=entity.answer,
            score=entity.score,
            answered_at=entity.answered_at
        )

    @staticmethod
    def beehive_detail_to_dto(entity: BeehiveDetailReport) -> BeehiveDetailReportDto:
        return BeehiveDetailReportDto(
            beehive=ReportMapper.beehive_info_to_dto(entity.beehive),
            questions_answers=[
                ReportMapper.question_answer_to_dto(qa)
                for qa in entity.questions_answers
            ]
        )

    @staticmethod
    def apiary_report_to_dto(entity: ApiaryReport) -> ApiaryReportDto:
        return ApiaryReportDto(
            apiary=ReportMapper.apiary_info_to_dto(entity.apiary),
            inventory=[
                ReportMapper.inventory_info_to_dto(inv)
                for inv in entity.inventory
            ],
            beehives=[
                ReportMapper.beehive_detail_to_dto(bh)
                for bh in entity.beehives
            ],
            total_questions=entity.total_questions,
            total_answers=entity.total_answers,
            generated_at=entity.generated_at
        )
