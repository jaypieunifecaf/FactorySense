"""
Interface de menu interativo para o sistema FactorySense.
"""

import sys
from typing import Optional
from ..services.quality_service import QualityService
from ..services.storage_service import StorageService
from ..reports.report_generator import ReportGenerator


class Menu:
    """
    Menu interativo para navegação no sistema.
    """

    def __init__(self):
        self.quality_service = QualityService()
        self.storage_service = StorageService()
        self.report_generator = ReportGenerator(
            self.quality_service,
            self.storage_service
        )
        self.running = True

    def display_header(self) -> None:
        """Exibe o cabeçalho do sistema."""
        print("\n" + "=" * 60)
        print("FACTORYSENSE - Sistema de Controle de Qualidade")
        print("=" * 60)

    def display_menu(self) -> None:
        """Exibe as opções do menu."""
        print("\nMENU PRINCIPAL:")
        print("  1. Cadastrar nova peça")
        print("  2. Listar peças aprovadas")
        print("  3. Listar peças reprovadas")
        print("  4. Remover peça")
        print("  5. Listar caixas fechadas")
        print("  6. Status da caixa atual")
        print("  7. Gerar relatório final")
        print("  8. Sair")
        print("-" * 60)

    def get_input(self, prompt: str, input_type=str, allow_empty: bool = False) -> any:
        """
        Obtém entrada do usuário com validação de tipo.

        Args:
            prompt: Mensagem para o usuário
            input_type: Tipo esperado (str, int, float)
            allow_empty: Permite entrada vazia

        Returns:
            Valor convertido para o tipo especificado
        """
        while True:
            try:
                value = input(prompt).strip()

                if not value and allow_empty:
                    return None

                if not value:
                    print("  ⚠ Entrada não pode ser vazia. Tente novamente.")
                    continue

                if input_type == str:
                    return value
                elif input_type == int:
                    return int(value)
                elif input_type == float:
                    return float(value)
                else:
                    return input_type(value)

            except ValueError:
                print(f"  ⚠ Valor inválido. Digite um {input_type.__name__} válido.")
            except KeyboardInterrupt:
                print("\n  ⚠ Operação cancelada.")
                return None

    def register_piece(self) -> None:
        """Registra uma nova peça no sistema."""
        print("\n" + "-" * 60)
        print("CADASTRAR NOVA PEÇA")
        print("-" * 60)

        try:
            # Obter dados da peça
            piece_id = self.get_input(
                "  ID da peça (deixe vazio para gerar automaticamente): ",
                allow_empty=True
            )
            weight = self.get_input("  Peso (em gramas): ", float)
            if weight is None:
                return

            color = self.get_input("  Cor: ", str)
            if not color:
                return

            length = self.get_input("  Comprimento (em cm): ", float)
            if length is None:
                return

            # Registrar peça
            piece = self.quality_service.register_piece(
                weight=weight,
                color=color,
                length=length,
                custom_id=piece_id if piece_id else None
            )

            # Exibir resultado
            print(f"\n  ✓ Peça {piece.piece_id} cadastrada com sucesso!")
            print(f"  Status: {piece.status.upper()}")

            if piece.is_rejected():
                print(f"  Motivo: {piece.rejection_reason}")
            else:
                # Tentar armazenar peça aprovada
                if self.storage_service.store_piece(piece):
                    current_box = self.storage_service.get_current_box()
                    if current_box:
                        print(f"  ✓ Peça armazenada na caixa #{current_box.box_id}")
                        print(f"  Ocupação: {current_box.get_piece_count()}/{current_box.capacity}")

                        if current_box.is_closed:
                            print(f"  ✓ Caixa #{current_box.box_id} foi fechada (completa)!")

        except Exception as e:
            print(f"  ✗ Erro ao cadastrar peça: {str(e)}")

    def list_approved_pieces(self) -> None:
        """Lista todas as peças aprovadas."""
        print("\n" + "-" * 60)
        print("PEÇAS APROVADAS")
        print("-" * 60)

        approved = self.quality_service.get_approved_pieces()

        if not approved:
            print("  Nenhuma peça aprovada registrada.")
            return

        print(f"\n  Total: {len(approved)} peça(s)\n")
        for piece in approved:
            print(f"  • {piece}")

    def list_rejected_pieces(self) -> None:
        """Lista todas as peças reprovadas com motivos."""
        print("\n" + "-" * 60)
        print("PEÇAS REPROVADAS")
        print("-" * 60)

        rejected = self.quality_service.get_rejected_pieces()

        if not rejected:
            print("  Nenhuma peça reprovada registrada.")
            return

        print(f"\n  Total: {len(rejected)} peça(s)\n")
        for piece in rejected:
            print(f"  • {piece}")

    def remove_piece(self) -> None:
        """Remove uma peça do registro."""
        print("\n" + "-" * 60)
        print("REMOVER PEÇA")
        print("-" * 60)

        all_pieces = self.quality_service.get_all_pieces()

        if not all_pieces:
            print("  Nenhuma peça registrada no sistema.")
            return

        # Mostrar peças disponíveis
        print("\n  Peças cadastradas:")
        for piece in all_pieces:
            print(f"  • {piece.piece_id} - {piece.status}")

        piece_id = self.get_input("\n  Digite o ID da peça a remover: ", str)
        if not piece_id:
            return

        if self.quality_service.remove_piece(piece_id):
            print(f"  ✓ Peça {piece_id} removida com sucesso!")
        else:
            print(f"  ✗ Peça {piece_id} não encontrada.")

    def list_closed_boxes(self) -> None:
        """Lista todas as caixas fechadas."""
        print("\n" + "-" * 60)
        print("CAIXAS FECHADAS")
        print("-" * 60)

        closed_boxes = self.storage_service.get_closed_boxes()

        if not closed_boxes:
            print("  Nenhuma caixa fechada no momento.")
            return

        print(f"\n  Total: {len(closed_boxes)} caixa(s)\n")
        for box in closed_boxes:
            print(f"  • {box}")
            # Mostrar primeiras peças da caixa
            if box.pieces:
                print(f"    Peças: {', '.join([p.piece_id for p in box.pieces[:5]])}", end="")
                if len(box.pieces) > 5:
                    print(f" ... (+{len(box.pieces) - 5})")
                else:
                    print()

    def show_current_box_status(self) -> None:
        """Mostra o status da caixa atual."""
        print("\n" + "-" * 60)
        print("STATUS DA CAIXA ATUAL")
        print("-" * 60)

        current_box = self.storage_service.get_current_box()

        if not current_box:
            print("  Nenhuma caixa em uso no momento.")
            return

        print(f"\n  Caixa: #{current_box.box_id}")
        print(f"  Status: {'FECHADA' if current_box.is_closed else 'ABERTA'}")
        print(f"  Ocupação: {current_box.get_piece_count()}/{current_box.capacity} peças")
        print(f"  Espaço disponível: {current_box.get_available_space()} peça(s)")

        if current_box.pieces:
            print(f"\n  Peças armazenadas:")
            for piece in current_box.pieces:
                print(f"    • {piece.piece_id}")

    def generate_final_report(self) -> None:
        """Gera e exibe o relatório final."""
        print("\n")
        print(self.report_generator.generate_summary_report())

    def run(self) -> None:
        """Executa o loop principal do menu."""
        self.display_header()

        while self.running:
            self.display_menu()

            choice = self.get_input("Escolha uma opção: ", str)

            if not choice:
                continue

            if choice == "1":
                self.register_piece()
            elif choice == "2":
                self.list_approved_pieces()
            elif choice == "3":
                self.list_rejected_pieces()
            elif choice == "4":
                self.remove_piece()
            elif choice == "5":
                self.list_closed_boxes()
            elif choice == "6":
                self.show_current_box_status()
            elif choice == "7":
                self.generate_final_report()
            elif choice == "8":
                self.exit_system()
            else:
                print("  ⚠ Opção inválida. Escolha um número entre 1 e 8.")

    def exit_system(self) -> None:
        """Finaliza o sistema."""
        print("\n" + "=" * 60)
        print("Encerrando FactorySense...")
        print("Obrigado por usar nosso sistema!")
        print("=" * 60 + "\n")
        self.running = False
        sys.exit(0)
