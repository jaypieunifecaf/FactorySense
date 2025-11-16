"""
Modelo de domínio para representar uma peça no sistema de controle de qualidade.
"""

from typing import Optional, Dict, Any


class Piece:
    """
    Representa uma peça individual a ser inspecionada.

    Atributos:
        piece_id: Identificador único da peça
        weight: Peso em gramas
        color: Cor da peça
        length: Comprimento em centímetros
        status: Status de aprovação ('aprovada' ou 'reprovada')
        rejection_reason: Motivo da reprovação (se aplicável)
    """

    def __init__(
        self,
        piece_id: str,
        weight: float,
        color: str,
        length: float,
        status: str = "pendente",
        rejection_reason: Optional[str] = None
    ):
        self.piece_id = piece_id
        self.weight = weight
        self.color = color.lower()
        self.length = length
        self.status = status
        self.rejection_reason = rejection_reason

    def to_dict(self) -> Dict[str, Any]:
        """Converte a peça para dicionário."""
        return {
            "id": self.piece_id,
            "peso": self.weight,
            "cor": self.color,
            "comprimento": self.length,
            "status": self.status,
            "motivo_reprovacao": self.rejection_reason
        }

    def approve(self) -> None:
        """Marca a peça como aprovada."""
        self.status = "aprovada"
        self.rejection_reason = None

    def reject(self, reason: str) -> None:
        """
        Marca a peça como reprovada.

        Args:
            reason: Motivo da reprovação
        """
        self.status = "reprovada"
        self.rejection_reason = reason

    def is_approved(self) -> bool:
        """Verifica se a peça está aprovada."""
        return self.status == "aprovada"

    def is_rejected(self) -> bool:
        """Verifica se a peça está reprovada."""
        return self.status == "reprovada"

    def __repr__(self) -> str:
        return (
            f"Piece(id={self.piece_id}, weight={self.weight}g, "
            f"color={self.color}, length={self.length}cm, status={self.status})"
        )

    def __str__(self) -> str:
        status_info = f" - {self.rejection_reason}" if self.rejection_reason else ""
        return (
            f"[{self.piece_id}] {self.weight}g, {self.color}, "
            f"{self.length}cm - {self.status.upper()}{status_info}"
        )
