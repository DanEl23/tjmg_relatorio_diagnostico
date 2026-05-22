# 🧪 ESPECIFICAÇÃO DOS TESTES

## 📍 Localização
- **Test 1**: `tests/unit/test_setup.py`
- **Test 2**: `tests/unit/test_generation.py`

**Tempo de execução**: Ambos < 5 segundos

---

## ✅ TEST 1: test_setup.py (Validação de Setup)

**Objetivo**: Verificar se toda a infraestrutura necessária está instalada e configurada corretamente antes de rodar o gerador principal.

**Tempo**: ~2 segundos

### ✔️ 5 Verificações Executadas:

#### **1️⃣ Testa importação de `preparar_dados_tabela_metas`**
```python
from src.core.generator import preparar_dados_tabela_metas
```
- **O que faz**: Tenta importar a função que prepara dados para tabelas de metas
- **Se falhar**: Programa para com erro
- **Se passar**: ✓ Função está disponível e acessível

#### **2️⃣ Testa importação de `adicionar_todas_metas_institucionais`**
```python
from src.tables.builders import adicionar_todas_metas_institucionais
```
- **O que faz**: Tenta importar a função que gera as 55 tabelas de metas
- **Se falhar**: Programa para com erro
- **Se passar**: ✓ Builder está implementado

#### **3️⃣ Verifica marcador em MAPA_RECURSOS**
```python
if "METAS_INSTITUCIONAIS" in MAPA_RECURSOS:
    config = MAPA_RECURSOS["METAS_INSTITUCIONAIS"]
```
- **O que faz**: Verifica se o marcador "METAS_INSTITUCIONAIS" está registrado no dicionário de recursos
- **Se passar**: Também exibe o tipo configurado
- **Resultado esperado**: `Tipo: METAS_INSTITUCIONAIS`

#### **4️⃣ Testa HISTORICO_METAS_CNJ**
```python
from src.content.static_data import HISTORICO_METAS_CNJ
total_metas = len(HISTORICO_METAS_CNJ)
```
- **O que faz**: Carrega os dados históricos de metas e conta quantas existem
- **Resultado esperado**: Total de metas (deve ser > 0)
- **Exibe**: Primeiras 5 metas encontradas (ex: Meta 1, Meta 2, Meta 3...)

#### **5️⃣ Testa função `preparar_dados_tabela_metas` com dados reais**
```python
dados = preparar_dados_tabela_metas("Meta 1")
```
- **O que faz**: Chama a função com um parâmetro real ("Meta 1") e verifica se retorna dados
- **Resultado esperado**: Retorna dados estruturados em linhas
- **Exibe**: Quantidade de linhas e amostra da primeira linha

### 🎯 Resultado Final:
```
✓ TODOS OS TESTES PASSARAM!
```

---

## ✅ TEST 2: test_generation.py (Teste Completo de Geração)

**Objetivo**: Fazer um teste COMPLETO de geração de um documento Word com as 55 metas, simulando o pipeline real.

**Tempo**: ~3 segundos

### ✔️ 7 Etapas Executadas:

#### **1️⃣ Cria documento de teste em memória**
```python
doc_teste = Document()
```
- **O que faz**: Cria um documento Word vazio
- **Resultado**: Documento pronto para receber tabelas

#### **2️⃣ Importa função de processamento e MAPA_RECURSOS**
```python
from src.core.generator import processar_recurso
from src.content.static_data import MAPA_RECURSOS
```
- **O que faz**: Carrega as funções necessárias para processar recursos
- **Relevância**: Simula o que o main.py faz

#### **3️⃣ Obtém configuração de METAS_INSTITUCIONAIS**
```python
config_metas = MAPA_RECURSOS.get("METAS_INSTITUCIONAIS")
```
- **O que faz**: Busca a configuração do marcador no dicionário
- **Validação**: Verifica se existe e não é nulа

#### **4️⃣ Chama processar_recurso (função principal)**
```python
processar_recurso(doc_teste, "METAS_INSTITUCIONAIS", config_metas, loader_jn=None)
```
- **O que faz**: AQUI OCORRE A MÁGICA! Esta é a função que:
  - Identifica que tipo é "METAS_INSTITUCIONAIS"
  - Chama `builders.adicionar_todas_metas_institucionais()`
  - Lê o Excel (exports/metas_institucionais_2025.xlsx)
  - Gera as 55 tabelas formatadas
  - Insere tudo no documento

#### **5️⃣ Analisa o documento gerado**
```python
total_paragrafos = len(doc_teste.paragraphs)
total_tabelas = len(doc_teste.tables)
```
- **O que faz**: Conta quantos parágrafos e tabelas foram adicionadas
- **Resultado esperado**: 
  - Muitos parágrafos (títulos + descrições + legendas)
  - Múltiplas tabelas (uma por meta)

#### **6️⃣ Exibe amostra do conteúdo gerado**
```python
for i, para in enumerate(doc_teste.paragraphs[:15]):
    if para.text.strip():
        print(f"   [{i}] {para.text}")
```
- **O que faz**: Mostra os primeiros 15 parágrafos
- **Resultado esperado**: Verá nomes de metas (TJMG 5, TJMG 6...) e descrições

#### **7️⃣ Salva o documento em arquivo**
```python
doc_teste.save("teste_metas_institucionais.docx")
```
- **O que faz**: Salva o documento gerado em disco
- **Localização**: Na raiz do projeto
- **Uso**: Você pode abrir em Word para inspecionar visualmente

### 🎯 Resultado Final:
```
✓ TESTE COMPLETO PASSOU COM SUCESSO!
```

---

## 🔄 Fluxo Resumido dos Testes

```
test_setup.py (Validação Rápida - 2s)
├─ 1. Importa preparar_dados_tabela_metas     ✓
├─ 2. Importa adicionar_todas_metas_institucionais ✓
├─ 3. Verifica METAS_INSTITUCIONAIS em MAPA_RECURSOS ✓
├─ 4. Carrega HISTORICO_METAS_CNJ             ✓
└─ 5. Testa preparar_dados_tabela_metas("Meta 1") ✓

test_generation.py (Teste Completo - 3s)
├─ 1. Cria documento vazio
├─ 2. Carrega processar_recurso()
├─ 3. Busca config de METAS_INSTITUCIONAIS
├─ 4. EXECUTA processar_recurso() ← PRINCIPAL
│  └─ Chama adicionar_todas_metas_institucionais()
│     └─ Lê Excel + Gera 55 tabelas
├─ 5. Conta parágrafos e tabelas
├─ 6. Mostra amostra do conteúdo
└─ 7. Salva em teste_metas_institucionais.docx
```

---

## 📊 O Que Cada Teste Valida

| Teste | Valida | Método | Tempo |
|-------|--------|--------|-------|
| **test_setup.py** | ✅ Setup correto | Import + função simples | ~2s |
| **test_generation.py** | ✅ Pipeline completo | Geração real com Excel | ~3s |

---

## 🚀 Como Usar

### **Executar test_setup (validação rápida)**
```bash
python tests/unit/test_setup.py
```
**Uso**: Verificar se tudo está instalado antes de rodar main.py

### **Executar test_generation (teste completo)**
```bash
python tests/unit/test_generation.py
```
**Uso**: Testar geração de documento sem executar main.py completo

### **Inspecionar resultado do teste**
```bash
# Após rodar test_generation, você terá este arquivo:
teste_metas_institucionais.docx
```
Abra em Word para ver o documento gerado com as 55 metas.

---

## ✅ Checklist de Saúde do Sistema

Use os testes assim:

```
ANTES de usar main.py:
  1. python tests/unit/test_setup.py        ← Verifica setup
  2. python tests/unit/test_generation.py   ← Verifica pipeline

Se ambos passarem (✓):
  3. python main.py                         ← Gera relatório completo
```

---

## 📈 Saídas Esperadas

### **test_setup.py - Saída esperada:**
```
======================================================================
TESTE: VERIFICAÇÃO DE IMPLEMENTAÇÃO DE METAS_INSTITUCIONAIS
======================================================================

✓ Testando importação de preparar_dados_tabela_metas...
  ✓ Função importada com sucesso

✓ Testando importação de adicionar_todas_metas_institucionais...
  ✓ Função importada com sucesso

✓ Testando marcador METAS_INSTITUCIONAIS em MAPA_RECURSOS...
  ✓ Marcador encontrado em MAPA_RECURSOS
  ✓ Tipo: METAS_INSTITUCIONAIS

✓ Testando HISTORICO_METAS_CNJ...
  ✓ Total de metas: 10
  ✓ Metas: Meta 1, Meta 2, Meta 3, Meta 4, Meta 5...

✓ Testando preparar_dados_tabela_metas com 'Meta 1'...
  ✓ Dados gerados: 3 linhas
  ✓ Primeira linha (cabeçalho): ['ANO', '...', ...]

======================================================================
✓ TODOS OS TESTES PASSARAM!
======================================================================
```

### **test_generation.py - Saída esperada:**
```
======================================================================
TESTE COMPLETO: GERAÇÃO DE METAS_INSTITUCIONAIS
======================================================================

1. Criando documento de teste...
   ✓ Documento criado

2. Importando função processar_recurso...
   ✓ Função e MAPA_RECURSOS importados

3. Obtendo configuração de METAS_INSTITUCIONAIS...
   ✓ Configuração obtida: tipo=METAS_INSTITUCIONAIS

4. Chamando processar_recurso com METAS_INSTITUCIONAIS...
   ✓ processar_recurso executado com sucesso

5. Analisando documento gerado...
   ✓ Parágrafos adicionados: 457
   ✓ Tabelas adicionadas: 55

6. Amostra do conteúdo gerado:
   [0] Meta 1
   [1] Descrição da Meta 1
   [2] [Tabela]
   [3] Fonte: ...
   ...

7. Salvando documento de teste...
   ✓ Documento salvo em: teste_metas_institucionais.docx

======================================================================
✓ TESTE COMPLETO PASSOU COM SUCESSO!
======================================================================
```

---

## 🎯 Resumo Executivo

| Aspecto | test_setup.py | test_generation.py |
|---------|--------------|------------------|
| **Propósito** | Validar setup | Testar geração |
| **Tempo** | ~2 segundos | ~3 segundos |
| **Verifica** | Imports + dados | Imports + Excel + Word |
| **Resultado** | ✓ Sistema pronto | ✓ Geração funciona |
| **Quando usar** | Antes de tudo | Teste rápido antes de main.py |
| **Valor** | Diagnóstico rápido | Teste end-to-end |

