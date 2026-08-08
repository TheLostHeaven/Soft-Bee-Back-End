from abc import ABC, abstractmethod
from uuid import UUID
from src.features.reports.domain.entities.apiary_report import ApiaryReport


class IReportService(ABC):
    """Interfaz para el servicio de reportes"""

    @abstractmethod
    def generate_apiary_report(self, apiary_id: UUID) -> ApiaryReport:
        """Genera un reporte completo del apiario"""
        pass
