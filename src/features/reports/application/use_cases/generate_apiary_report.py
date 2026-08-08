from uuid import UUID
from src.features.reports.domain.services.report_service import IReportService
from src.features.reports.application.dto.apiary_report_dto import ApiaryReportDto
from src.features.reports.application.mappers.report_mapper import ReportMapper


class GenerateApiaryReport:
    """Caso de uso para generar un reporte completo del apiario"""

    def __init__(self, report_service: IReportService):
        self.report_service = report_service

    def execute(self, apiary_id: UUID) -> ApiaryReportDto:
        """
        Genera un reporte completo del apiario
        
        Args:
            apiary_id: ID del apiario
            
        Returns:
            ApiaryReportDto con toda la información del apiario
        """
        report_entity = self.report_service.generate_apiary_report(apiary_id)
        return ReportMapper.apiary_report_to_dto(report_entity)
