"""
Serviço de controle de qualidade para gerenciamento de peças.
"""

from typing import List, Dict, Any
from ..models.piece import Piece
from ..validators.quality_validator import QualityValidator


class QualityService:
    """
    Gerencia o processo de inspeção e classificação de peças.
    """

    def __init__(self):
        self.pieces: List[Piece] = []
        self._next_piece_number = 1

    def register_piece(
        self,
        weight: float,
        color: str,
        length: float,
        custom_id: str = None
    ) -> Piece:
        """
        Registra uma nova peça e aplica validação de qualidade.

        Args:
            weight: Peso da peça em gramas
            color: Cor da peça
            length: Comprimento da peça em centímetros
            custom_id: ID personalizado (opcional)

        Returns:
            Peça registrada e validada
        """
        # Gerar ID se não fornecido
        if custom_id is None:
            custom_id = f"P{self._next_piece_number:03d}"
            self._next_piece_number += 1

        # Criar peça
        piece = Piece(
            piece_id=custom_id,
            weight=weight,
            color=color,
            length=length
        )

        # Aplicar validação
        QualityValidator.apply_validation(piece)

        # Registrar peça
        self.pieces.append(piece)

        return piece

    def remove_piece(self, piece_id: str) -> bool:
        """
        Remove uma peça do registro.

        Args:
            piece_id: ID da peça a ser removida

        Returns:
            True se removida, False se não encontrada
        """
        for i, piece in enumerate(self.pieces):
            if piece.piece_id == piece_id:
                self.pieces.pop(i)
                return True
        return False

    def get_approved_pieces(self) -> List[Piece]:
        """Retorna lista de peças aprovadas."""
        return [p for p in self.pieces if p.is_approved()]

    def get_rejected_pieces(self) -> List[Piece]:
        """Retorna lista de peças reprovadas."""
        return [p for p in self.pieces if p.is_rejected()]

    def get_piece_by_id(self, piece_id: str) -> Piece:
        """
        Busca uma peça por ID.

        Args:
            piece_id: ID da peça

        Returns:
            Peça encontrada ou None
        """
        for piece in self.pieces:
            if piece.piece_id == piece_id:
                return piece
        return None

    def get_all_pieces(self) -> List[Piece]:
        """Retorna todas as peças registradas."""
        return self.pieces.copy()

    def get_statistics(self) -> Dict[str, Any]:
        """
        Retorna estatísticas consolidadas.

        Returns:
            Dicionário com estatísticas das peças
        """
        approved = self.get_approved_pieces()
        rejected = self.get_rejected_pieces()

        # Consolidar motivos de reprovação
        rejection_reasons = {}
        for piece in rejected:
            if piece.rejection_reason:
                # Extrair cada motivo individual
                reasons = piece.rejection_reason.split("; ")
                for reason in reasons:
                    rejection_reasons[reason] = rejection_reasons.get(reason, 0) + 1

        return {
            "total_pieces": len(self.pieces),
            "approved_count": len(approved),
            "rejected_count": len(rejected),
            "rejection_reasons": rejection_reasons,
            "approval_rate": len(approved) / len(self.pieces) * 100 if self.pieces else 0
        }

    def clear_all(self) -> None:
        """Limpa todos os registros de peças."""
        self.pieces.clear()
        self._next_piece_number = 1
