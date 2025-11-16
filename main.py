#!/usr/bin/env python3
"""
FactorySense - Sistema de Automação para Controle de Qualidade e Armazenamento de Peças

Aplicação principal que inicializa o sistema de controle de qualidade industrial.

Autor: João Paulo
Versão: 1.0
Data: 2025
"""

import sys
from src.cli.menu import Menu


def main():
    """
    Função principal que inicializa o sistema FactorySense.
    """
    try:
        # Inicializar e executar o menu interativo
        menu = Menu()
        menu.run()

    except KeyboardInterrupt:
        print("\n\nSistema interrompido pelo usuário.")
        print("Encerrando FactorySense...\n")
        sys.exit(0)

    except Exception as e:
        print(f"\n✗ Erro crítico no sistema: {str(e)}")
        print("Por favor, verifique a configuração e tente novamente.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
