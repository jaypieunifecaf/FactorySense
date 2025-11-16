"""
Validador de qualidade para inspeção de peças.
"""

from typing import Tuple, Optional
from ..models.piece import Piece


class QualityValidator:
    """
    Valida peças de acordo com as regras de qualidade estabelecidas.

    Regras de aprovação:
    - Peso: 95g a 105g
    - Cor: azul ou verde
    - Comprimento: 10cm a 20cm
    """

    # Constantes de validação
    MIN_WEIGHT = 95
    MAX_WEIGHT = 105
    VALID_COLORS = {"azul", "verde"}
    MIN_LENGTH = 10
    MAX_LENGTH = 20

    @classmethod
    def validate(cls, piece: Piece) -> Tuple[bool, Optional[str]]:
        """
        Valida uma peça de acordo com as regras de qualidade.

        Args:
            piece: Peça a ser validada

        Returns:
            Tupla (is_approved, rejection_reason)
            - is_approved: True se aprovada, False se reprovada
            - rejection_reason: Motivo da reprovação (None se aprovada)
        """
        reasons = []

        # Validar peso
        if not cls._validate_weight(piece.weight):
            reasons.append(
                f"Peso fora do padrão ({piece.weight}g - permitido: "
                f"{cls.MIN_WEIGHT}g a {cls.MAX_WEIGHT}g)"
            )

        # Validar cor
        if not cls._validate_color(piece.color):
            reasons.append(
                f"Cor inválida ('{piece.color}' - permitidas: "
                f"{', '.join(sorted(cls.VALID_COLORS))})"
            )

        # Validar comprimento
        if not cls._validate_length(piece.length):
            reasons.append(
                f"Comprimento fora do padrão ({piece.length}cm - permitido: "
                f"{cls.MIN_LENGTH}cm a {cls.MAX_LENGTH}cm)"
            )

        if reasons:
            return False, "; ".join(reasons)

        return True, None

    @classmethod
    def _validate_weight(cls, weight: float) -> bool:
        """Valida o peso da peça."""
        return cls.MIN_WEIGHT <= weight <= cls.MAX_WEIGHT

    @classmethod
    def _validate_color(cls, color: str) -> bool:
        """Valida a cor da peça."""
        return color.lower() in cls.VALID_COLORS

    @classmethod
    def _validate_length(cls, length: float) -> bool:
        """Valida o comprimento da peça."""
        return cls.MIN_LENGTH <= length <= cls.MAX_LENGTH

    @classmethod
    def apply_validation(cls, piece: Piece) -> None:
        """
        Aplica a validação e atualiza o status da peça.

        Args:
            piece: Peça a ser validada
        """
        is_approved, rejection_reason = cls.validate(piece)

        if is_approved:
            piece.approve()
        else:
            piece.reject(rejection_reason)
