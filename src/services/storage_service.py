"""
Serviço de armazenamento para gerenciamento de caixas.
"""

from typing import List, Optional
from ..models.piece import Piece
from ..models.box import Box


class StorageService:
    """
    Gerencia o armazenamento de peças aprovadas em caixas.
    """

    def __init__(self, box_capacity: int = Box.DEFAULT_CAPACITY):
        self.box_capacity = box_capacity
        self.boxes: List[Box] = []
        self.current_box: Optional[Box] = None
        self._next_box_id = 1

    def store_piece(self, piece: Piece) -> bool:
        """
        Armazena uma peça aprovada na caixa atual.

        Args:
            piece: Peça a ser armazenada

        Returns:
            True se armazenada com sucesso, False caso contrário
        """
        if not piece.is_approved():
            return False

        # Criar primeira caixa se necessário
        if self.current_box is None:
            self._create_new_box()

        # Tentar adicionar à caixa atual
        if self.current_box.add_piece(piece):
            # Se a caixa ficou cheia, criar nova
            if self.current_box.is_full():
                self._create_new_box()
            return True

        return False

    def _create_new_box(self) -> Box:
        """Cria uma nova caixa e a define como atual."""
        new_box = Box(box_id=self._next_box_id, capacity=self.box_capacity)
        self.boxes.append(new_box)

        # Atualizar caixa atual apenas se a anterior estava fechada ou não existia
        if self.current_box is None or self.current_box.is_closed:
            self.current_box = new_box

        self._next_box_id += 1
        return new_box

    def get_closed_boxes(self) -> List[Box]:
        """Retorna lista de caixas fechadas."""
        return [box for box in self.boxes if box.is_closed]

    def get_open_boxes(self) -> List[Box]:
        """Retorna lista de caixas abertas."""
        return [box for box in self.boxes if not box.is_closed]

    def get_all_boxes(self) -> List[Box]:
        """Retorna todas as caixas."""
        return self.boxes.copy()

    def get_current_box(self) -> Optional[Box]:
        """Retorna a caixa atual em uso."""
        return self.current_box

    def get_total_stored_pieces(self) -> int:
        """Retorna o total de peças armazenadas em todas as caixas."""
        return sum(box.get_piece_count() for box in self.boxes)

    def get_statistics(self) -> dict:
        """
        Retorna estatísticas de armazenamento.

        Returns:
            Dicionário com estatísticas das caixas
        """
        closed_boxes = self.get_closed_boxes()
        open_boxes = self.get_open_boxes()

        return {
            "total_boxes": len(self.boxes),
            "closed_boxes": len(closed_boxes),
            "open_boxes": len(open_boxes),
            "total_stored_pieces": self.get_total_stored_pieces(),
            "current_box_fill": (
                self.current_box.get_piece_count() if self.current_box else 0
            ),
            "current_box_capacity": (
                self.current_box.capacity if self.current_box else 0
            )
        }

    def clear_all(self) -> None:
        """Limpa todos os registros de caixas."""
        self.boxes.clear()
        self.current_box = None
        self._next_box_id = 1
