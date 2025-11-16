# FactorySense

Sistema de Automação para Controle de Qualidade e Armazenamento de Peças

## Visão Geral

FactorySense é um sistema desenvolvido em Python para automatizar o processo de inspeção de peças em linhas de montagem industriais. O sistema realiza validação automática de qualidade, classificação de peças e gerenciamento inteligente de caixas de armazenamento.

## Problema Resolvido

O processo manual de inspeção industrial apresenta diversos desafios:
- Atrasos devido à conferência manual
- Falhas de qualidade por erro humano
- Falta de padronização na inspeção
- Armazenamento desorganizado
- Dificuldade em gerar relatórios consolidados

## Objetivos

- Automatizar a verificação de qualidade das peças
- Organizar o armazenamento de peças aprovadas
- Reduzir intervenção humana em tarefas repetitivas
- Fornecer relatórios consolidados para tomada de decisão
- Demonstrar como Python pode suportar automação industrial

## Funcionalidades

### Cadastro e Validação de Peças
- Cadastro de peças com ID, peso, cor e comprimento
- Validação automática baseada em regras de qualidade
- Classificação automática (aprovada/reprovada)
- Registro detalhado de motivos de reprovação

### Regras de Qualidade

Uma peça é **aprovada** se atender todos os critérios:
- Peso: 95g a 105g
- Cor: azul ou verde
- Comprimento: 10cm a 20cm

Caso contrário, é **reprovada** com o motivo registrado.

### Gerenciamento de Caixas
- Armazenamento automático de peças aprovadas
- Capacidade padrão: 10 peças por caixa
- Fechamento automático ao atingir capacidade
- Criação automática de nova caixa
- Rastreamento de caixas abertas e fechadas

### Operações Disponíveis
1. Cadastrar nova peça
2. Listar peças aprovadas
3. Listar peças reprovadas (com motivos)
4. Remover peça do registro
5. Listar caixas fechadas
6. Ver status da caixa atual
7. Gerar relatório final completo
8. Sair do sistema

## Requisitos

- Python 3.7 ou superior
- Nenhuma dependência externa necessária (usa apenas biblioteca padrão)

## Instalação

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd FactorySense
```

2. Verifique a versão do Python:
```bash
python3 --version
```

## Como Usar

### Executar o Sistema

```bash
python3 main.py
```

### Exemplo de Uso

```
============================================================
FACTORYSENSE - Sistema de Controle de Qualidade
============================================================

MENU PRINCIPAL:
  1. Cadastrar nova peça
  2. Listar peças aprovadas
  3. Listar peças reprovadas
  4. Remover peça
  5. Listar caixas fechadas
  6. Status da caixa atual
  7. Gerar relatório final
  8. Sair
------------------------------------------------------------
Escolha uma opção: 1

------------------------------------------------------------
CADASTRAR NOVA PEÇA
------------------------------------------------------------
  ID da peça (deixe vazio para gerar automaticamente):
  Peso (em gramas): 100
  Cor: azul
  Comprimento (em cm): 15

  ✓ Peça P001 cadastrada com sucesso!
  Status: APROVADA
  ✓ Peça armazenada na caixa #1
  Ocupação: 1/10
```

## Estrutura do Projeto

```
FactorySense/
├── main.py                    # Ponto de entrada da aplicação
├── README.md                  # Documentação
├── requirements.txt           # Dependências (vazio - usa stdlib)
└── src/
    ├── __init__.py
    ├── models/               # Modelos de domínio
    │   ├── __init__.py
    │   ├── piece.py         # Modelo de Peça
    │   └── box.py           # Modelo de Caixa
    ├── validators/          # Validadores de qualidade
    │   ├── __init__.py
    │   └── quality_validator.py
    ├── services/            # Lógica de negócio
    │   ├── __init__.py
    │   ├── quality_service.py    # Gerenciamento de peças
    │   └── storage_service.py    # Gerenciamento de caixas
    ├── reports/             # Geração de relatórios
    │   ├── __init__.py
    │   └── report_generator.py
    └── cli/                 # Interface de linha de comando
        ├── __init__.py
        └── menu.py
```

## Arquitetura

### Modelos de Domínio

**Piece (Peça)**
```python
{
  "id": "P001",
  "peso": 100,
  "cor": "azul",
  "comprimento": 15,
  "status": "aprovada",
  "motivo_reprovacao": None
}
```

**Box (Caixa)**
- ID único
- Capacidade de 10 peças
- Lista de peças armazenadas
- Status (aberta/fechada)

### Camadas

1. **Models**: Entidades de domínio (Piece, Box)
2. **Validators**: Regras de negócio para validação
3. **Services**: Lógica de aplicação (QualityService, StorageService)
4. **Reports**: Geração de relatórios e estatísticas
5. **CLI**: Interface de usuário textual

## Exemplos de Cenários

### Cenário 1: Peça Aprovada

```
Entrada:
  Peso: 100g
  Cor: verde
  Comprimento: 15cm

Resultado:
  ✓ Status: APROVADA
  ✓ Armazenada na caixa atual
```

### Cenário 2: Peça Reprovada

```
Entrada:
  Peso: 120g (fora da faixa)
  Cor: vermelho (cor inválida)
  Comprimento: 8cm (abaixo do mínimo)

Resultado:
  ✗ Status: REPROVADA
  Motivos:
    - Peso fora do padrão (120g - permitido: 95g a 105g)
    - Cor inválida ('vermelho' - permitidas: azul, verde)
    - Comprimento fora do padrão (8cm - permitido: 10cm a 20cm)
```

### Cenário 3: Fechamento Automático de Caixa

```
Ao cadastrar a 10ª peça aprovada:
  ✓ Peça P010 cadastrada com sucesso!
  ✓ Peça armazenada na caixa #1
  ✓ Caixa #1 foi fechada (completa)!

Próxima peça aprovada:
  ✓ Peça armazenada na caixa #2
  Ocupação: 1/10
```

## Relatório Final

O sistema gera relatórios completos com:

```
============================================================
RELATÓRIO FINAL - FACTORYSENSE
Sistema de Controle de Qualidade e Armazenamento
============================================================

RESUMO DE PEÇAS:
  • Total de peças cadastradas: 25
  • Peças aprovadas: 18 (72.0%)
  • Peças reprovadas: 7 (28.0%)

MOTIVOS DE REPROVAÇÃO:
  • Peso fora do padrão: 4 peça(s)
  • Cor inválida: 2 peça(s)
  • Comprimento fora do padrão: 3 peça(s)

ARMAZENAMENTO:
  • Total de caixas utilizadas: 2
  • Caixas fechadas: 1
  • Caixas abertas: 1
  • Total de peças armazenadas: 18
  • Caixa atual: 8/10 peças

============================================================
```

## Boas Práticas Implementadas

### Código
- Modularização em funções e classes
- Documentação com docstrings
- Type hints para clareza
- Separação de responsabilidades (SRP)
- Nomenclatura descritiva em português

### Arquitetura
- Separação em camadas (models, services, validators, reports, cli)
- Baixo acoplamento entre módulos
- Alta coesão dentro dos módulos
- Princípios SOLID aplicados

### Validação
- Validação de entrada de dados
- Tratamento de exceções
- Feedback claro ao usuário
- Consistência nas mensagens

## Possíveis Expansões

### Integração com Hardware
- Sensores de peso automáticos
- Leitores de código de barras
- Sistemas de visão computacional para cor
- Medidores laser de comprimento

### Inteligência Artificial
- Detecção de defeitos visuais com CNN
- Previsão de falhas com ML
- Otimização de parâmetros de qualidade
- Análise preditiva de tendências

### Funcionalidades Adicionais
- Persistência em banco de dados
- Interface web com dashboard
- Exportação de relatórios (PDF, Excel)
- Sistema de usuários e permissões
- Integração com ERP
- API RESTful para integração
- Rastreabilidade completa (lote, data, operador)
- Alertas em tempo real

## Benefícios

### Operacionais
- Redução de 90%+ no tempo de inspeção
- Eliminação de erros humanos na validação
- Padronização completa do processo
- Rastreabilidade total das peças

### Estratégicos
- Dados para tomada de decisão
- Identificação de padrões de falha
- Base para otimização contínua
- Conformidade com ISO 9001

## Autor

**João Paulo**
Versão 1.0 - 2025

## Licença

Projeto educacional desenvolvido como protótipo de automação industrial.

## Suporte

Para dúvidas ou sugestões, abra uma issue no repositório do projeto.
