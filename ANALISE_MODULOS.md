# 📦 ANÁLISE DE MÓDULOS PYTHON - NECESSIDADE E IMPACTO

## Status Geral
- **Total de .py na raiz**: 23 arquivos
- **Necessários**: 5-6 arquivos
- **Opcionais**: 2-3 arquivos (para testes)
- **Obsoletos**: 12-15 arquivos (desenvolvimento/debug)
- **Data**: 22 de Abril de 2026

---

## 📊 CATEGORIZAÇÃO DETALHADA

### ✅ NECESSÁRIOS E ATIVOS (6 arquivos)

| # | Arquivo | Propósito | Status | Razão |
|---|---------|----------|--------|-------|
| 1 | **main.py** | Entrada principal do programa | ✅ **MANTER** | Executa toda a geração de relatórios |
| 2 | **integrador_jira.py** | Integração com JIRA | ✅ **MANTER** | Importa dados de JIRA (importado em processar_dados) |
| 3 | **migrar_arquivos.py** | Migração de arquivos | ✅ **MANTER** | Utilitário de migração para o pipeline |
| 4 | **processar_dados.py** | Processamento dados brutos | ✅ **MANTER** | Preprocessamento de dados antes de relatório |
| 5 | **teste_tabelas.py** | Testes de tabelas | ⚠️ **REVISAR** | Verificar se ainda está em uso |
| 6 | **teste_tabela_meta_unica_anos.py** | Teste de tabelas por ano | ⚠️ **REVISAR** | Verificar se ainda está em uso |

---

### ⚠️ OPCIONAIS - TESTES ÚTEIS (2 arquivos)

| # | Arquivo | Propósito | Status | Recomendação |
|---|---------|----------|--------|--------------|
| 1 | **test_metas_check.py** | Validação rápida de setup | ✅ **ÚTIL** | Manter para validação pré-implementação |
| 2 | **test_metas_geracao.py** | Teste completo de geração | ✅ **ÚTIL** | Manter para validação de relatórios |

**Recomendação**: Mover para diretório `tests/` para organização

---

### ❌ OBSOLETOS - SCRIPTS DE DESENVOLVIMENTO (15 arquivos)

Todos esses arquivos foram criados durante o PROCESSO DE DESENVOLVIMENTO para:
- Adicionar/corrigir marcadores
- Debugar problemas de formatação
- Validar específicos aspetos da implementação
- São executados UMA VEZ e nunca mais

#### **Grupo 1: Scripts de Adição de Marcadores (3 arquivos)**
```
adicionar_marcador_metas.py      ❌ Executado 1x → Marcador adicionado
add_marcador_v2.py                ❌ Executado 1x → Versão melhorada
analisar_marcadores.py            ❌ Script de debug/análise
```
**Por que obsoletos**: Marcador já está em Conteudo_Fonte.docx. Não precisa rodar novamente.

#### **Grupo 2: Scripts de Correção de Problemas (2 arquivos)**
```
corrigir_marcador.py              ❌ Executado 1x → Problema resolvido
corrigir_formato_marcador.py      ❌ Executado 1x → Problema resolvido
```
**Por que obsoletos**: Já corrigiram seus problemas. Código está correto agora.

#### **Grupo 3: Scripts de Validação/Verificação (10 arquivos)**
```
validar_relatorio_com_metas.py    ❌ Debug específico
validar_detalhado.py               ❌ Validação detalhada
verificar_alinhamento_vertical.py  ❌ Verificação de formatação
verificar_alturas_legenda.py       ❌ Verificação de alturas das linhas
verificar_break_prevention.py      ❌ Verificação de page breaks
verificar_conteudo_fonte.py        ❌ Análise de conteúdo
verificar_formatacao_detalhada.py  ❌ Debug de formatação
verificar_formatacao_tabelas.py    ❌ Debug de formatação
verificar_marcador.py              ❌ Verificação de marcador
debug_row_heights.py               ❌ Debug de alturas
```
**Por que obsoletos**: Serviam para debugar formatação de tabelas durante desenvolvimento. 
Agora que tudo funciona, não precisam rodar.

#### **Grupo 4: Testes Antigos (1 arquivo)**
```
validar_final.py                   ❌ Teste de validação
```
**Por que obsoleto**: Substituído por test_metas_check.py e test_metas_geracao.py

---

## 🎯 IMPACTO DE CADA CATEGORIA

### NECESSÁRIOS (main.py, integrador_jira.py, etc.)
- **Impacto**: CRÍTICO
- **Se deletar**: Sistema quebra
- **Status**: Todos importados por main.py ou pipeline principal

### OPCIONAIS (test_*.py)
- **Impacto**: NENHUM (são apenas testes)
- **Se deletar**: Perde capacidade de validação rápida
- **Recomendação**: Mover para `tests/unit/` e renomear com padrão pytest

### OBSOLETOS (verificar_*, validar_*, corrigir_*, etc.)
- **Impacto**: NENHUM
- **Se deletar**: Ambiente mais limpo, sem confusão
- **Recomendação**: Mover para `_archived/` ou deletar

---

## 📋 VERIFICAÇÃO DE IMPORTS (O que está realmente em uso?)

```bash
# Verificar o que main.py importa
grep -r "^import\|^from" main.py | head -20

# Verificar o que é importado em src/
grep -r "integrador_jira\|migrar_arquivos\|processar_dados" src/
```

---

## ✅ RECOMENDAÇÃO DE AÇÃO

### MANTER (em raiz)
```
✅ main.py                    [Essencial - entrada principal]
✅ integrador_jira.py         [Essencial - integração]
✅ migrar_arquivos.py         [Essencial - utilitário]
✅ processar_dados.py         [Essencial - processamento]
```

### REVISAR (verificar se em uso)
```
⚠️  teste_tabelas.py          [Verificar imports]
⚠️  teste_tabela_meta_unica_anos.py [Verificar imports]
```

### MOVER PARA tests/unit/
```
📦 test_metas_check.py        → tests/unit/test_setup.py
📦 test_metas_geracao.py      → tests/unit/test_generation.py
```

### DELETAR (sem necessidade)
```
❌ adicionar_marcador_metas.py
❌ add_marcador_v2.py
❌ analisar_marcadores.py
❌ corrigir_marcador.py
❌ corrigir_formato_marcador.py
❌ debug_row_heights.py
❌ validar_detalhado.py
❌ validar_final.py
❌ validar_relatorio_com_metas.py
❌ verificar_alinhamento_vertical.py
❌ verificar_alturas_legenda.py
❌ verificar_break_prevention.py
❌ verificar_conteudo_fonte.py
❌ verificar_formatacao_detalhada.py
❌ verificar_formatacao_tabelas.py
❌ verificar_marcador.py
```

**Total a deletar**: 16 arquivos

---

## 🔍 ANÁLISE POR TIPO DE ARQUIVO

### **Arquivo: main.py**
```python
Status:     ✅ NECESSÁRIO
Imports:    src/config, src/content/static_data, src/core/generator, src/extractors/pdf_extractor
Dependentes: Tudo depende disso
Ação:       MANTER
```

### **Arquivo: integrador_jira.py**
```python
Status:     ✅ NECESSÁRIO (potencial)
Imports:    jira, etc
Usado por:  processar_dados.py (potencialmente)
Ação:       MANTER (verificar se importado em pipeline)
```

### **Arquivo: migrar_arquivos.py**
```python
Status:     ✅ NECESSÁRIO
Propósito:  Migration utility
Ação:       MANTER
```

### **Arquivo: processar_dados.py**
```python
Status:     ✅ NECESSÁRIO
Propósito:  Data processing pipeline
Ação:       MANTER
```

### **Arquivo: test_metas_check.py**
```python
Status:     ✅ ÚTIL
Propósito:  Validação rápida
Execução:   < 5 segundos
Recomendação: Mover para tests/ e renomear
```

### **Arquivo: test_metas_geracao.py**
```python
Status:     ✅ ÚTIL
Propósito:  Teste completo de geração
Execução:   < 2 segundos
Recomendação: Mover para tests/ e renomear
```

### **Arquivos: verificar_*.py, validar_*.py, debug_*.py**
```python
Status:     ❌ OBSOLETOS
Propósito:  Debug/validation durante desenvolvimento
Versionamento: v1.0 (durante testes)
Recomendação: DELETAR
```

---

## 📈 ESTRUTURA PROPOSTA APÓS LIMPEZA

```
tjmg_relatorio_diagnostico/
├── main.py                        [Entrada principal]
├── integrador_jira.py            [Integração JIRA]
├── migrar_arquivos.py            [Utilitário]
├── processar_dados.py            [Processamento]
├── teste_tabelas.py              [Verificar necessidade]
├── teste_tabela_meta_unica_anos.py [Verificar necessidade]
│
├── tests/
│   ├── unit/
│   │   ├── test_setup.py          [← test_metas_check.py]
│   │   └── test_generation.py     [← test_metas_geracao.py]
│   └── integration/
│
├── src/
│   ├── core/
│   ├── extractors/
│   ├── tables/
│   └── ...
│
├── README.md
├── FLUXO_METAS_INSTITUCIONAIS.md
└── MAPEAMENTO_MD.md
```

---

## 🗑️ LIMPEZA EM 3 ETAPAS

### **Etapa 1: Deletar Obsoletos (16 arquivos)**
```bash
# Scripts de desenvolvimento que já foram executados
rm adicionar_marcador_metas.py add_marcador_v2.py analisar_marcadores.py \
   corrigir_marcador.py corrigir_formato_marcador.py debug_row_heights.py \
   validar_detalhado.py validar_final.py validar_relatorio_com_metas.py \
   verificar_alinhamento_vertical.py verificar_alturas_legenda.py \
   verificar_break_prevention.py verificar_conteudo_fonte.py \
   verificar_formatacao_detalhada.py verificar_formatacao_tabelas.py \
   verificar_marcador.py
```

### **Etapa 2: Verificar Necessidade (2 arquivos)**
```bash
# Executar para ver se funcionam e são necessários
python teste_tabelas.py
python teste_tabela_meta_unica_anos.py

# Se erro ou não necessário, deletar
# Se funcionam, manter ou mover para tests/
```

### **Etapa 3: Organizar Testes (2 arquivos - Opcional)**
```bash
# Criar diretório se não existir
mkdir -p tests/unit

# Mover/renomear testes
mv test_metas_check.py tests/unit/test_setup.py
mv test_metas_geracao.py tests/unit/test_generation.py
```

---

## ⏱️ TEMPO ESTIMADO

| Ação | Tempo |
|------|-------|
| Deletar 16 arquivos | 1 min |
| Verificar 2 arquivos | 2 min |
| Organizar testes | 1 min |
| **Total** | **~4 minutos** |

---

## 📝 RESUMO EXECUTIVO

| Métrica | Valor |
|---------|-------|
| Total de .py criados | 23 |
| Necessários | 4 (essencial) + 2 (integração) = 6 |
| Opcionais | 2 (testes) |
| Obsoletos | 15 |
| **A Deletar** | **16** |
| **A Manter** | **4** |
| **A Revisar** | **2** |
| **A Reorganizar** | **2** |

