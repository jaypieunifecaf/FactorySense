"""
Gerador de relatórios do sistema de controle de qualidade.
"""

from typing import Dict, Any
from ..services.quality_service import QualityService
from ..services.storage_service import StorageService


class ReportGenerator:
    """
    Gera relatórios consolidados do sistema.
    """

    def __init__(self, quality_service: QualityService, storage_service: StorageService):
        self.quality_service = quality_service
        self.storage_service = storage_service

    def generate_summary_report(self) -> str:
        """
        Gera relatório resumido com todas as estatísticas.

        Returns:
            String formatada com o relatório completo
        """
        quality_stats = self.quality_service.get_statistics()
        storage_stats = self.storage_service.get_statistics()

        report_lines = [
            "=" * 60,
            "RELATÓRIO FINAL - FACTORYSENSE",
            "Sistema de Controle de Qualidade e Armazenamento",
            "=" * 60,
            "",
            "RESUMO DE PEÇAS:",
            f"  • Total de peças cadastradas: {quality_stats['total_pieces']}",
            f"  • Peças aprovadas: {quality_stats['approved_count']} "
            f"({quality_stats['approval_rate']:.1f}%)",
            f"  • Peças reprovadas: {quality_stats['rejected_count']} "
            f"({100 - quality_stats['approval_rate']:.1f}%)",
            "",
        ]

        # Adicionar motivos de reprovação
        if quality_stats['rejection_reasons']:
            report_lines.append("MOTIVOS DE REPROVAÇÃO:")
            for reason, count in sorted(
                quality_stats['rejection_reasons'].items(),
                key=lambda x: x[1],
                reverse=True
            ):
                report_lines.append(f"  • {reason}: {count} peça(s)")
            report_lines.append("")

        # Adicionar informações de armazenamento
        report_lines.extend([
            "ARMAZENAMENTO:",
            f"  • Total de caixas utilizadas: {storage_stats['total_boxes']}",
            f"  • Caixas fechadas: {storage_stats['closed_boxes']}",
            f"  • Caixas abertas: {storage_stats['open_boxes']}",
            f"  • Total de peças armazenadas: {storage_stats['total_stored_pieces']}",
        ])

        if storage_stats['current_box_fill'] > 0:
            report_lines.append(
                f"  • Caixa atual: {storage_stats['current_box_fill']}/"
                f"{storage_stats['current_box_capacity']} peças"
            )

        report_lines.extend([
            "",
            "=" * 60,
        ])

        return "\n".join(report_lines)

    def get_consolidated_data(self) -> Dict[str, Any]:
        """
        Retorna dados consolidados em formato estruturado.

        Returns:
            Dicionário com todos os dados do sistema
        """
        return {
            "quality": self.quality_service.get_statistics(),
            "storage": self.storage_service.get_statistics(),
            "pieces": {
                "approved": [p.to_dict() for p in self.quality_service.get_approved_pieces()],
                "rejected": [p.to_dict() for p in self.quality_service.get_rejected_pieces()],
            }
        }
