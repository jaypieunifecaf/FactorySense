"""
Modelo de domínio para representar caixas de armazenamento de peças.
"""

from typing import List
from .piece import Piece


class Box:
    """
    Representa uma caixa para armazenar peças aprovadas.

    Atributos:
        box_id: Identificador único da caixa
        capacity: Capacidade máxima de peças (padrão: 10)
        pieces: Lista de peças armazenadas
        is_closed: Indica se a caixa está fechada
    """

    DEFAULT_CAPACITY = 10

    def __init__(self, box_id: int, capacity: int = DEFAULT_CAPACITY):
        self.box_id = box_id
        self.capacity = capacity
        self.pieces: List[Piece] = []
        self.is_closed = False

    def add_piece(self, piece: Piece) -> bool:
        """
        Adiciona uma peça à caixa se houver espaço.

        Args:
            piece: Peça a ser adicionada

        Returns:
            True se a peça foi adicionada, False se a caixa está cheia
        """
        if self.is_full() or self.is_closed:
            return False

        if not piece.is_approved():
            return False

        self.pieces.append(piece)

        if self.is_full():
            self.close()

        return True

    def is_full(self) -> bool:
        """Verifica se a caixa está cheia."""
        return len(self.pieces) >= self.capacity

    def close(self) -> None:
        """Fecha a caixa."""
        self.is_closed = True

    def get_piece_count(self) -> int:
        """Retorna a quantidade de peças na caixa."""
        return len(self.pieces)

    def get_available_space(self) -> int:
        """Retorna o espaço disponível na caixa."""
        return self.capacity - len(self.pieces)

    def __repr__(self) -> str:
        status = "FECHADA" if self.is_closed else "ABERTA"
        return f"Box(id={self.box_id}, pieces={len(self.pieces)}/{self.capacity}, status={status})"

    def __str__(self) -> str:
        status = "FECHADA" if self.is_closed else "ABERTA"
        return f"Caixa #{self.box_id}: {len(self.pieces)}/{self.capacity} peças - {status}"
