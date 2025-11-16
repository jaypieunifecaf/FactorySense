#!/usr/bin/env python3
"""
Script de teste básico para validar funcionalidades principais do FactorySense.
"""

from src.models.piece import Piece
from src.models.box import Box
from src.validators.quality_validator import QualityValidator
from src.services.quality_service import QualityService
from src.services.storage_service import StorageService
from src.reports.report_generator import ReportGenerator


def test_piece_creation():
    """Testa criação de peças."""
    print("Testando criação de peças...")
    piece = Piece("P001", 100, "azul", 15)
    assert piece.piece_id == "P001"
    assert piece.weight == 100
    assert piece.color == "azul"
    assert piece.length == 15
    print("  ✓ Criação de peça funcionando")


def test_quality_validation():
    """Testa validação de qualidade."""
    print("\nTestando validação de qualidade...")

    # Peça aprovada
    piece1 = Piece("P001", 100, "azul", 15)
    QualityValidator.apply_validation(piece1)
    assert piece1.is_approved()
    print("  ✓ Peça válida aprovada corretamente")

    # Peça reprovada - peso
    piece2 = Piece("P002", 200, "azul", 15)
    QualityValidator.apply_validation(piece2)
    assert piece2.is_rejected()
    print("  ✓ Peça com peso inválido reprovada corretamente")

    # Peça reprovada - cor
    piece3 = Piece("P003", 100, "vermelho", 15)
    QualityValidator.apply_validation(piece3)
    assert piece3.is_rejected()
    print("  ✓ Peça com cor inválida reprovada corretamente")

    # Peça reprovada - comprimento
    piece4 = Piece("P004", 100, "azul", 5)
    QualityValidator.apply_validation(piece4)
    assert piece4.is_rejected()
    print("  ✓ Peça com comprimento inválido reprovada corretamente")


def test_box_storage():
    """Testa armazenamento em caixas."""
    print("\nTestando armazenamento em caixas...")

    box = Box(1, capacity=3)  # Caixa pequena para teste

    # Adicionar peças aprovadas
    for i in range(3):
        piece = Piece(f"P{i+1:03d}", 100, "verde", 15)
        piece.approve()
        result = box.add_piece(piece)
        assert result is True

    assert box.is_full()
    assert box.is_closed
    print("  ✓ Caixa fechada automaticamente ao atingir capacidade")


def test_quality_service():
    """Testa serviço de qualidade."""
    print("\nTestando serviço de qualidade...")

    service = QualityService()

    # Registrar peças
    piece1 = service.register_piece(100, "azul", 15)
    piece2 = service.register_piece(200, "vermelho", 5)

    assert len(service.get_all_pieces()) == 2
    assert len(service.get_approved_pieces()) == 1
    assert len(service.get_rejected_pieces()) == 1
    print("  ✓ Serviço de qualidade funcionando corretamente")


def test_storage_service():
    """Testa serviço de armazenamento."""
    print("\nTestando serviço de armazenamento...")

    storage = StorageService(box_capacity=3)

    # Criar e armazenar peças aprovadas
    for i in range(5):
        piece = Piece(f"P{i+1:03d}", 100, "azul", 15)
        piece.approve()
        storage.store_piece(piece)

    # Deve ter criado 2 caixas (3 + 2 peças)
    assert len(storage.get_all_boxes()) == 2
    assert len(storage.get_closed_boxes()) == 1
    print("  ✓ Serviço de armazenamento funcionando corretamente")


def test_report_generation():
    """Testa geração de relatórios."""
    print("\nTestando geração de relatórios...")

    quality_service = QualityService()
    storage_service = StorageService()
    report_gen = ReportGenerator(quality_service, storage_service)

    # Adicionar algumas peças
    quality_service.register_piece(100, "azul", 15)  # Aprovada
    quality_service.register_piece(200, "vermelho", 5)  # Reprovada

    # Armazenar aprovada
    for piece in quality_service.get_approved_pieces():
        storage_service.store_piece(piece)

    report = report_gen.generate_summary_report()
    assert "RELATÓRIO FINAL" in report
    assert "RESUMO DE PEÇAS" in report
    print("  ✓ Geração de relatórios funcionando corretamente")


def main():
    """Executa todos os testes."""
    print("=" * 60)
    print("FACTORYSENSE - TESTES BÁSICOS")
    print("=" * 60)

    try:
        test_piece_creation()
        test_quality_validation()
        test_box_storage()
        test_quality_service()
        test_storage_service()
        test_report_generation()

        print("\n" + "=" * 60)
        print("✓ TODOS OS TESTES PASSARAM COM SUCESSO!")
        print("=" * 60 + "\n")

    except AssertionError as e:
        print(f"\n✗ Teste falhou: {str(e)}\n")
        return 1
    except Exception as e:
        print(f"\n✗ Erro durante testes: {str(e)}\n")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
