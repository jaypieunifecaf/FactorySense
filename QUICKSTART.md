# FactorySense - Guia de Início Rápido

## Começando em 3 Passos

### 1. Execute a Aplicação

```bash
python3 main.py
```

### 2. Experimente um Fluxo de Exemplo

#### Registrar uma Peça Aprovada
```
Escolha uma opção: 1
ID: (pressione Enter para gerar automaticamente)
Peso: 100
Cor: azul
Comprimento: 15

Resultado: ✓ APROVADA e armazenada na caixa
```

#### Registrar uma Peça Reprovada
```
Escolha uma opção: 1
ID: (pressione Enter)
Peso: 200
Cor: vermelho
Comprimento: 5

Resultado: ✗ REPROVADA com motivos detalhados
```

#### Visualizar Relatório
```
Escolha uma opção: 7

Veja estatísticas completas e análises
```

### 3. Explore as Funcionalidades

**Opções do Menu:**
1. **Cadastrar Peça** - Adicione novas peças com validação automática
2. **Listar Aprovadas** - Veja todas as peças que passaram no controle de qualidade
3. **Listar Reprovadas** - Veja falhas com motivos de reprovação
4. **Remover Peça** - Exclua uma peça do sistema
5. **Listar Caixas Fechadas** - Visualize caixas de armazenamento completas
6. **Status da Caixa Atual** - Verifique a capacidade da caixa ativa
7. **Gerar Relatório** - Estatísticas completas do sistema
8. **Sair** - Feche a aplicação

## Dados de Teste de Exemplo

### Peças Válidas (Serão APROVADAS)
```
Peso: 100g, Cor: azul, Comprimento: 15cm
Peso: 95g, Cor: verde, Comprimento: 10cm
Peso: 105g, Cor: azul, Comprimento: 20cm
```

### Peças Inválidas (Serão REPROVADAS)
```
Peso: 120g, Cor: azul, Comprimento: 15cm    → Peso fora do padrão
Peso: 100g, Cor: vermelho, Comprimento: 15cm → Cor inválida
Peso: 100g, Cor: azul, Comprimento: 5cm      → Comprimento fora do padrão
```

## Regras de Qualidade

**Uma peça é APROVADA se:**
- Peso: 95g a 105g
- Cor: azul OU verde
- Comprimento: 10cm a 20cm

**Caso contrário: REPROVADA** (com motivo detalhado)

## Gerenciamento de Caixas

- Cada caixa comporta exatamente 10 peças aprovadas
- Quando cheia, a caixa fecha automaticamente
- Nova caixa abre automaticamente
- Apenas peças aprovadas são armazenadas

## Executando os Testes

```bash
python3 test_basic.py
```

Saída esperada:
```
✓ TODOS OS TESTES PASSARAM COM SUCESSO!
```

## Exemplo de Sessão

```
============================================================
FACTORYSENSE - Sistema de Controle de Qualidade
============================================================

MENU PRINCIPAL:
  1. Cadastrar nova peça
  ...

Escolha uma opção: 1

CADASTRAR NOVA PEÇA
  ID da peça (deixe vazio para gerar automaticamente):
  Peso (em gramas): 100
  Cor: azul
  Comprimento (em cm): 15

  ✓ Peça P001 cadastrada com sucesso!
  Status: APROVADA
  ✓ Peça armazenada na caixa #1
  Ocupação: 1/10

# ... cadastre mais 9 peças aprovadas ...

  ✓ Peça P010 cadastrada com sucesso!
  Status: APROVADA
  ✓ Peça armazenada na caixa #1
  ✓ Caixa #1 foi fechada (completa)!

# ... próxima peça aprovada cria nova caixa ...

  ✓ Peça P011 cadastrada com sucesso!
  Status: APROVADA
  ✓ Peça armazenada na caixa #2
  Ocupação: 1/10
```

## Solução de Problemas

**P: Erro de versão do Python?**
```bash
python3 --version  # Deve ser 3.7 ou superior
```

**P: Erros de importação?**
```bash
# Certifique-se de estar no diretório raiz do projeto
cd /caminho/para/FactorySense
python3 main.py
```

**P: Quer resetar os dados?**
Apenas reinicie a aplicação - os dados são mantidos apenas em memória

## Próximos Passos

1. Execute a aplicação e experimente
2. Teste diferentes configurações de peças
3. Preencha uma caixa completa (10 peças)
4. Gere relatórios para ver as estatísticas
5. Leia o README.md para documentação detalhada
6. Confira o IMPLEMENTATION.md para detalhes técnicos

## Suporte

Para dúvidas ou problemas, consulte:
- README.md - Documentação completa do usuário
- IMPLEMENTATION.md - Detalhes técnicos de implementação
- Comentários no código fonte - Documentação inline

---

**Bons Testes!** 🏭
