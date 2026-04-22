# TJMG Relatório Diagnóstico - Sistema de Automação de Relatórios

## 📋 Visão Geral do Projeto

**TJMG Relatório Diagnóstico** é um sistema integrado de **automação e processamento de relatórios diagnósticos** para o Tribunal de Justiça de Minas Gerais (TJMG). O projeto combina extração de dados de múltiplas fontes (PDF, Excel, CSV, APIs), processamento inteligente de metadados, e geração dinâmica de documentos Word profissionais com incorporação de gráficos, tabelas, e indicadores.

### Objetivos Principais
- ✅ Extrair automaticamente dados de justiça (CNJ - Conselho Nacional de Justiça)
- ✅ Processar indicadores de desempenho e estrutura judiciária
- ✅ Gerar relatórios Word profissionais com tabelas e imagens formatadas
- ✅ Mapear e incorporar gráficos dinâmicos do PDF "Justiça em Números"
- ✅ Manter sincronização com metadados via JIRA (pipeline de suporte)
- ✅ Aplicar estilos visuais institucionais TJMG (branding)

---

## 🏗️ Arquitetura do Projeto

```
tjmg_relatorio_diagnostico/
├── main.py                        # Ponto de entrada principal
├── requirements.txt               # Dependências Python
├── integrador_jira.py            # Extrator de dados JIRA
├── migrar_arquivos.py            # Script de migração
├── processar_dados.py            # Processamento de dados brutos
├── teste_tabelas.py              # Testes de tabelas
│
├── src/                          # Código-fonte da arquitetura modular
│   ├── __init__.py
│   ├── config.py                 # Configuração centralizada (caminhos, cores, padrões)
│   │
│   ├── content/                  # Dados estáticos e conteúdo
│   │   ├── static_data.py        # Tabelas hardcoded (Atos, Áreas, Estruturas)
│   │   └── __init__.py
│   │
│   ├── core/                     # Núcleo de geração do relatório
│   │   ├── generator.py          # Motor principal (gerar_relatorio_completo)
│   │   ├── styles.py             # Estilos visuais TJMG
│   │   └── __init__.py
│   │
│   ├── extractors/               # Extratores de dados multi-fonte
│   │   ├── cnj_loader.py         # Carrega dados do CSV CNJ
│   │   ├── jn_loader.py          # Loader "Justiça em Números" com mapa de métricas
│   │   ├── excel_loader.py       # Carrega e processa Excel (ASPLAG)
│   │   ├── pdf_extractor.py      # Extrai imagens/gráficos do PDF via PyMuPDF
│   │   ├── extracao_cnj.py       # Automação Selenium para portal CNJ
│   │   ├── process_extractor.py  # Extrator de processos da planilha
│   │   ├── mapeador_meta*.py     # Mapeadores específicos de metas CNJ
│   │   └── __init__.py
│   │
│   ├── media/                    # Gestão de mídia (imagens)
│   │   ├── images.py             # Inserção de imagens com legendas
│   │   └── __init__.py
│   │
│   ├── tables/                   # Construção de tabelas Word
│   │   ├── builders.py           # Construtores de tabelas (15+ tipos)
│   │   ├── utils.py              # Utilitários de formatação XML
│   │   └── __init__.py
│   │
│   ├── tools/                    # Ferramentas diagnósticas
│   │   ├── diagnose_pdf.py       # Análise de estrutura PDF
│   │   ├── diagnostico_metadados.py
│   │   ├── explorar_planilha.py
│   │   ├── extract_pdf_pages.py
│   │   └── __init__.py
│   │
│   └── utils/                    # Utilitários gerais
│       ├── image_matcher.py      # Correspondência de gráficos (similaridade)
│       └── __init__.py
│
├── data/                         # Dados estruturados
│   ├── raw/                      # Dados de entrada
│   │   ├── JN_15-Jan-2026.csv   # Dado CNJ (15 cols: sigla, ano, cn, cp, etc)
│   │   ├── dados_manuais.csv    # Métricas manuais (rankings, tempos, %)
│   │   ├── Metricas_JN_CNJ.ini  # Dicionário de métricas (mapeamento coluna→métrica)
│   │   ├── Conteudo_Fonte.docx  # Template Word com marcadores
│   │   ├── Sumario_Modelo.docx  # Modelo de sumário visual
│   │   ├── Informações TJMG_ASPLAG resposta do CEINFO.xlsx
│   │   └── 15-jan-2026/         # Dados históricos por data
│   │
│   └── processed/               # Dados processados
│       ├── dicionario_graficos.json       # Mapeamento gráficos PDF → nomes
│       ├── mapeamento_graficos_completo.json
│       ├── canvas_images/                # Gráficos canvas (processados)
│       ├── extracted_images/             # Imagens extraídas do PDF
│       ├── jn_images/                    # Imagens Justiça em Números
│       └── output/                       # Relatório final gerado
│
├── exports/                      # Exportações finais
│   ├── dicionario_metas_hierarquico.json
│   ├── html_jira.html
│   └── [Outros resultados de extração]
│
├── resources/                    # Recursos estáticos (capa, logos)
│   └── capa_relatorio.png
│
├── Notebooks/                    # Análise exploratória
│   ├── tratamento.ipynb          # Processamento de dados, metas
│   ├── gráficos.ipynb            # Análise gráfica
│   ├── graficos_2.ipynb
│   └── data/                     # Dados dos notebooks
│
├── tests/                        # Testes unitários/integração
│   ├── integration/
│   └── unit/
│
└── tools/                        # Scripts auxiliares diversos
```

---

## 🔄 Fluxo de Processamento Principal

### 1. **Inicialização** (`main.py`)
```
main() 
├─ Argumento: --extrair (força extração PDF) ou --saida (nome arquivo final)
├─ Verifica se existem imagens extraídas em data/processed/extracted_images/
├─ Se não existir ou --extrair ativado: Executa extrair_imagens()
└─ Chama gerar_relatorio_completo() com MAPA_RECURSOS
```

### 2. **Extração de Imagens** (`pdf_extractor.py`)
```
extrair_imagens()
├─ Abre PDF via PyMuPDF (fitz)
├─ Itera por páginas procurando por regex: "Figura|Gráfico|Quadro"
├─ Detecta legendas no texto do PDF
├─ Faz crop da imagem (400px acima da legenda até a legenda)
├─ Salva em data/processed/extracted_images/
└─ Gera JSON: mapeamento_graficos_completo.json
```

### 3. **Carregamento de Dados** 
```
CarregadorJN (jn_loader.py)
├─ Carrega CSV: data/raw/JN_15-Jan-2026.csv (CNJ)
├─ Carrega CSV: data/raw/dados_manuais.csv (Métricas manuais)
├─ Mantém MAPA_METRICAS: ~100 métricas mapeadas (cn→casos_novos, etc)
├─ Implementa _obter_valor() com fallback Manual→CNJ
└─ Implementa _formatar() com padrão brasileiro (1.000,00 ou 75,3%)

CNJDataLoader (cnj_loader.py)
├─ Carrega CSV do CNJ
├─ Extrai dados para tribunal específico (sigla='TJMG')
├─ Calcula ranking de porte (Grande/Médio/Pequeno)
└─ Retorna dicionário com 20+ métricas formatadas
```

### 4. **Geração do Relatório** (`generator.py` → `gerar_relatorio_completo()`)
```
gerar_relatorio_completo(caminho_base_dummy, output_path, mapa_recursos)
├─ 1. Setup: Document Word vazio
│  └─ configurar_layout_pagina(): A4, margens ABNT (3cm/2cm)
│  └─ configurar_estilos_tjmg(): Heading 1/2/3 em cor vinho #A21612
│  └─ adicionar_paginacao_rodape(): Campo PAGE no rodapé direito
│  
├─ 2. Insere Capa: capa_relatorio.png (21cm width)
│  
├─ 3. Processa Sumário Visual: copia página do Sumario_Modelo.docx
│  
├─ 4. Processa Conteúdo: Lê Conteudo_Fonte.docx parágrafo por parágrafo
│  └─ Detecta marcadores especiais:
│     • Títulos (regex: "^(\d+(?:\.\d+)*\.?)\s+(.*)") → Heading 1/2/3
│     • Recurso Visual (texto == chave em MAPA_RECURSOS) → processar_recurso()
│     • Listas ([INICIAR_LISTA_NUMERICA], [INICIAR_LISTA_MARCADORES])
│     • Quebra de página ([QUEBRA_PAGINA])
│     • Ícones ([ICON_CHECK] → ✓ verde)
│     • Notas ([MARK_NOTA] → formato pequeno)
│  
└─ 5. Salva: .docx em data/output/[nome_saida]
```

### 5. **Processamento de Recursos** (`processar_recurso()`)
```
Tipos de Recursos Suportados:
├─ IMAGEM
│  └─ images.adicionar_imagem(): busca em DIR_CANVAS_IMAGES, insere com legenda
│
├─ TABELA_ORAS (Orçamento)
│  ├─ TABELA_ORCAMENTO_CONJUNTO
│  ├─ TABELA_ORCAMENTO_DETALHADA
│  └─ TABELA_ORCAMENTO (com fonte custom)
│
├─ TABELA_SIMPLES
│  ├─ TABELA_SIMPLES_3COL: 3 colunas com header cinza
│  ├─ TABELA_4COL_SIMPLES: 4 colunas (Comarcas)
│  ├─ TABELA_6COL_SIMPLES: 6 colunas
│  └─ Suporta indent/recuo customizado
│
├─ TABELA_COMPARATIVO_TEMAS
│  └─ Tabela comparativa com temas TJMG
│
└─ TABELA_METAS_DINAMICA
   ├─ Meta COM subgrupos (Meta 4): 2 cabeçalhos, múltiplas instâncias
   ├─ Meta SIMPLES (Meta 1,2,3): cabeçalho único, instâncias
   └─ Integra dados de resultados_cnj.xlsx (2025*)
```

---

## 📊 Módulos Principais

### **src/config.py** - Configuração Centralizada
```python
# Caminhos
BASE_DIR, DATA_DIR, RAW_DIR, PROCESSED_DIR, OUTPUT_DIR

# Cores TJMG
Colors.TJMG_BLUE = "44546A"      # Azul escuro (cabeçalhos)
Colors.HEADER_GRAY = "7F7F7F"    # Cinza médio
Colors.ZEBRA_STRIPE = "EEEEEE"   # Fundo alternado linhas

# Layout ABNT
Layout.MARGIN_TOP = 3.0 cm
Layout.MARGIN_LEFT = 3.0 cm
Layout.MARGIN_RIGHT = 2.0 cm

# Padrões Regex
Patterns.TITULO: "^\s*(\d+(?:\.\d{1,2})*\.?)\s+([A-Z].*)"
Patterns.PDF_GRAPH_LEGEND: "(Figura|Gráfico|Quadro)\s+\d+"
```

### **src/content/static_data.py** - Dados Hardcoded
```python
# Tabelas pré-formatadas como listas de tuplas
dados_tabela_atos = [
  ("Lei Complementar nº 59/2001", "Contém organização e divisão..."),
  ...
]

dados_tabela_areas = [
  ("HEADER_MAIN", "DENOMINAÇÃO", "SIGLA"),
  ("DATA_SPLIT", "Assessoria de Precatórios", "ASPREC"),
  ...
]

# Mapa de recursos (Tabelas, Imagens, Dados dinâmicos)
MAPA_RECURSOS = {
  "Tabela Atos Normativos": {
    "tipo": "TABELA_ATOS",
    "dados": dados_tabela_atos
  },
  "Gráfico Estrutura": {
    "tipo": "IMAGEM",
    "arquivo": "estrutura.png",
    "fonte": "Própria"
  },
  ...
}
```

### **src/extractors/jn_loader.py** - Carregador CNJ com Mapeamento
```python
class CarregadorJN:
  def __init__(self, caminho_csv_dados, caminho_csv_manual):
    self.mapa_metricas = {
      "casos_novos": "cn",           # Campo CSV
      "casos_pendentes": "cp",
      "cn_100k_hab": "ch",
      "perc_eletr": ("cnelet", "cn"),  # Cálculo: divisão
      "perc_cargos_vagos_mag": ("magv", "mag"),
      ...
    }
  
  def _obter_valor(self, df_ano, coluna):
    # 1. Tenta buscar no manual (dados_manuais.csv)
    # 2. Fallback para CNJ (JN_15-Jan-2026.csv)
    # 3. Retorna 0 se não encontrar
  
  def _formatar(self, valor, is_percent=False):
    # Converte para padrão BR: 1.000,00 ou 75,3%
  
  def carregar():
    # Detecta separador/encoding automaticamente
    # Converte números BR para float
```

### **src/core/generator.py** - Motor Principal
```python
def gerar_relatorio_completo(caminho_base_dummy, output_path, mapa_recursos):
  # 1. Configura layout (A4, margens)
  # 2. Insere capa
  # 3. Lê Conteudo_Fonte.docx
  # 4. Processa cada parágrafo:
  #    - Detecta títulos / recursos visuais / listas
  #    - Chama processar_recurso() para tabelas/imagens
  # 5. Salva documento final
  
def processar_recurso(doc, chave, item, loader_jn=None):
  # Dispatcher para diferentes tipos de tabelas/imagens
  # Passa loader_jn para acesso a dados dinâmicos

def preparar_dados_tabela_metas(nome_meta):
  # Processa Meta 1-8
  # Lê dados históricos + 2025 (resultados_cnj.xlsx)
  # Formata com cabeçalhos e instâncias específicas
```

### **src/tables/builders.py** - Construtores de Tabelas
```python
# 15+ Funções específicas:

def adicionar_tabela_atos(document, dados):
  # Tabela 01: 2 colunas, header cinza, zebra stripe

def adicionar_tabela_areas(document, dados):
  # Tabela 02: 2 colunas, sem bordas, grupos com borda superior

def adicionar_tabela_simples_3col(document, dados, titulo_custom, indent_cm):
  # 3 colunas com largura 8cm, 4cm, 4cm

def adicionar_tabela_4col_simples(document, dados, titulo_custom, larguras):
  # 4 colunas (Comarcas), larguras customizáveis

def adicionar_tabela_metas_dinamica(document, dados_processados):
  # Metas CNJ: cabeçalho complexo (2 linhas), instâncias, cores

def adicionar_tabela_orcamento_conjunto(document, dados):
  # Orçamento: múltiplas colunas, sublinha de totais

# Utils XML para formatação fino:
def set_cell_vertical_alignment(cell, align)
def set_row_height_at_least(row, height_twips)
def set_cell_bottom_border(cell)
def set_group_top_border(cell)
def remove_all_borders(cell)
def aplicar_recuo_tabela(table, recuo_cm)  # Recuo/indentação de tabela
```

### **src/media/images.py** - Gestão de Imagens
```python
def adicionar_imagem(document, nome_arquivo, titulo="", fonte="Própria", 
                     largura_custom=None, recuo_esq=0, space_after=None):
  # 1. Busca em DIR_CANVAS_IMAGES
  # 2. Insere com parágrafo (com recuo opcional)
  # 3. Adiciona legenda em pt 9 com fonte
  # 4. Espaçamento configurável
```

### **src/extractors/pdf_extractor.py** - Extração de PDFs
```python
def extrair_imagens():
  # 1. Abre PDF (PyMuPDF)
  # 2. Itera páginas procurando "Figura|Gráfico" no texto
  # 3. Faz crop da imagem (rect 30px margens, 400px acima legenda)
  # 4. Salva PNG em 150 DPI
  # 5. Gera JSON: {"Figura 01": {"pagina": 10, "caminho": "...", "status": "encontrado"}}
```

### **src/utils/image_matcher.py** - Correspondência de Gráficos
```python
def extrair_numero_grafico(texto):
  # "Gráfico 78" → 78

def calcular_similaridade(str1, str2):
  # SequenceMatcher para busca fuzzy

def encontrar_arquivo_por_numero(numero, arquivos):
  # Padrão: "Gráfico {numero} - Descrição_PgXXX_FINAL.png"

def encontrar_melhor_correspondencia(numero, arquivos, threshold=0.8):
  # Fallback se busca exata falhar
```

---

## 🔌 Fluxo de Dados e Transformações

### Input Data Formats

#### 1. **CSV CNJ** (`data/raw/JN_15-Jan-2026.csv`)
Formato: Separador `;` ou `,` (detectado auto), encoding `latin1`

Colunas principais:
```
justica,sigla,uf,ano,comarca,varaje,mag,magv,ts,tfaux,servadmseti,
cn,cp,ch,ipm,ipsjud,iad,tc,tcl,effmedia,cnelet,j100_perc,
...
```

Exemplo:
```
Estadual,TJMG,MG,2025,796,5234,501,12,4230,890,32,
156000,498000,650,85.2,78.5,96.3,42.1,38.9,68.5,156784,...
```

#### 2. **CSV Manual** (`data/raw/dados_manuais.csv`)
Formato: Métricas que não existem no CNJ ou valores especiais

Colunas:
```
ano,pop_sede_perc,j100_perc,n4,bv,serv1_perc,t_giro,tm_fis,tm_elet,ranking_manual,custo_magistrado,custo_servidor,tempo_sent_1,tempo_sent_2
```

Exemplo:
```
2025,82.0,91.2,20,1509,86.0,3a e 2m,s/d,s/d,2º lugar,100713,29093,2a e 6m,6m
```

#### 3. **Excel ASPLAG** (`data/raw/Informações TJMG_ASPLAG resposta do CEINFO.xlsx`)
Abas: "Estrutura e Força de Trabalho", "Movimentação Processual", etc.
Usado para: Dados complementares, gráficos canvas

#### 4. **Word Conteúdo Fonte** (`data/raw/Conteudo_Fonte.docx`)
Estrutura de marcadores para integração:
- Títulos em padrão numérico: "1. INTRODUÇÃO", "2.1 Subtítulo"
- Chaves de recursos: "Tabela Atos Normativos", "Gráfico Estrutura"
- Marcadores especiais: [QUEBRA_PAGINA], [ICON_CHECK], [INICIAR_LISTA_NUMERICA]

#### 5. **PDF Justiça em Números** (`data/raw/justica-em-numeros-2025.pdf`)
Fonte de: Gráficos dinâmicos, legendas com padrão "Figura XX", dimensões

### Output Data Formats

#### 1. **Relatório Final** (`data/output/Relatorio_Final_Completo.docx`)
- Documento Word .docx com formatação completa
- Capa + Sumário + Conteúdo com tabelas, imagens, estilos
- Paginação automática no rodapé

#### 2. **JSON Mapeamento Gráficos** (`data/processed/mapeamento_graficos_completo.json`)
```json
{
  "Figura 01": {
    "pagina": 45,
    "caminho_completo": "/path/to/extracted_images/Figura 01.png",
    "status": "encontrado"
  },
  "Figura 02": {...}
}
```

#### 3. **Dicionários Estáticos** (`data/processed/dicionario_graficos.json`)
Mapeamento: "Gráfico Relatório" → "Gráfico PDF Original"

---

## 🛠️ Dependências e Tecnologias

### Python Packages (requirements.txt)
```
docx==0.2.4                      # Manipulação de .docx (baixo nível)
python-docx==1.1.0              # Manipulação de .docx (API)
PyMuPDF==1.26.7 (fitz)          # Extração de PDF
openpyxl==3.1.5                 # Leitura Excel (XLSX)
pandas==2.3.3                   # Processamento de dados
pillow==12.1.0                  # Processamento de imagens
lxml==6.0.2                     # Parser XML (para Word OOXML)
numpy==2.4.0                    # Computação numérica
pytz==2025.2                    # Timezones
python-dateutil==2.9.0.post0    # Manipulação de datas
typing_extensions==4.15.0       # Type hints
```

### Arquiteturas de Software
- **Modular**: Separação clara entre extraction, processing, generation
- **Pipeline Orientado**: Dados fluem por estágios distintos
- **Loose Coupling**: Módulos podem ser testados independentemente
- **Resource Map Pattern**: MAPA_RECURSOS centraliza configuração de conteúdo

### Principais Bibliotecas por Função
| Função | Biblioteca |
|--------|-----------|
| Manipulação Word | python-docx |
| Extração PDF | PyMuPDF (fitz) |
| Processamento Dados | pandas, numpy |
| Imagens | Pillow |
| XML/OOXML | lxml |
| Excel | openpyxl |
| Automação Web (futuro) | selenium, BeautifulSoup |

---

## 🎯 Features Principais

### 1. **Extração Inteligente de Dados**
- ✅ Carregamento automático de CSV com detecção de separador/encoding
- ✅ Fallback Manual→CNJ para métricas com dados faltantes
- ✅ Mapeamento de ~100 métricas judiciais (IPM, IPS, TCL, etc)
- ✅ Parsing de números em formato brasileiro (1.000,00)

### 2. **Geração Dinâmica de Tabelas**
- ✅ 15+ tipos de tabelas com formatação específica
- ✅ Headers customizáveis (cinza, azul, vinho)
- ✅ Zebra stripe (alternância de cores de linha)
- ✅ Suporte a merged cells, sublinha, borders customizados
- ✅ Recuo/indentação de tabelas (para estruturas aninhadas)
- ✅ Altura de linha automática ou fixa

### 3. **Processamento de Imagens**
- ✅ Extração automática de gráficos/figuras do PDF
- ✅ Correspondência de imagens com similaridade fuzzy
- ✅ Inserção com legendas e recuo customizável
- ✅ Suporte a múltiplos formatos (PNG, JPEG)

### 4. **Branding e Estilos TJMG**
- ✅ Cores institucionais (azul #44546A, cinza #7F7F7F, vinho #A21612)
- ✅ Fonte Calibri em todos os textos
- ✅ Heading 1/2/3 com cor vinho e espaçamento ABNT
- ✅ Margens A4: 3cm (superior/esquerda), 2cm (inferior/direita)

### 5. **Processamento Avançado de Conteúdo**
- ✅ Regex sophisticated para detecção de títulos (1.2.3. TITULO)
- ✅ Suporte a listas numeradas e com marcadores
- ✅ Saltos de página automáticos via [QUEBRA_PAGINA]
- ✅ Ícones Unicode (✓ checkmark em verde)
- ✅ Notes formatadas (pt 10, espaçamento reduzido)

### 6. **Pipeline de Dados Híbrido**
- ✅ Dados estruturados (CSV) + semi-estruturados (Wood) + estáticos (hardcoded)
- ✅ Suporte a metadados via JIRA (futuro completo)
- ✅ Processamento notebook exploratorio (Jupyter)
- ✅ Exportações em múltiplos formatos (DOCX, JSON, XLSX)

---

## 📈 Processamento de Metas CNJ

### Estrutura de Metas
```python
HISTORICO_METAS_CNJ = {
  "Meta 1": {
    "descricao": "Manter a taxa de congestionamento...",
    "objetivo": 75.0,
    "dados_passados": {
      "1º Grau": [85.2, 84.1, 82.5, 81.0],
      "2º Grau": [42.1, 41.5, 40.8, 39.5],
      "Geral": [62.3, 61.8, 60.2, 58.5]
    }
  },
  "Meta 4": {
    "descricao": "Aumentar práticas de conciliação...",
    "grupos": [
      {
        "nome": "Clovis Pires (NUCIF 4.0)",
        "dados": {"1º Grau": [...], "2º Grau": [...], "Meta": [...]}
      },
      ...
    ]
  },
  ...
}
```

### Geração de Tabelas de Metas
1. Carrega histórico estático (2021-2024)
2. Busca resultado 2025 em `exports/resultados_cnj.xlsx`
3. Monta cabeçalho: "META | DESCRIÇÃO | [SUBGRUPO] | INSTÂNCIA | HISTÓRICO | 2021 | 2022 | 2023 | 2024 | 2025*"
4. Preenchimento de dados com formatos especiais (%, números, "---")

---

## 🔧 Configuração e Uso

### Instalação
```bash
# Clone o repositório
git clone <repo>
cd tjmg_relatorio_diagnostico

# Crie um ambiente virtual
python -m venv venv
source venv/Scripts/activate  # Windows
# ou: source venv/bin/activate  # Linux/Mac

# Instale dependências
pip install -r requirements.txt
```

### Uso Básico
```bash
# Gera relatório com extração forçada de imagens
python main.py --extrair

# Gera relatório com nome customizado
python main.py --saida "Relatorio_2025.docx"

# Gera relatório pulando extração (se imagens já existem)
python main.py
```

### Estrutura de Arquivo de Entrada

O arquivo Word de entrada (`Conteudo_Fonte.docx`) deve conter:

```
1. INTRODUÇÃO
Texto de introdução aqui...

1.1 Contexto
Texto contexto...

[QUEBRA_PAGINA]

2. ESTRUTURA DO TRIBUNAL

Tabela Atos Normativos

Algum texto narrativo.

Gráfico Estrutura Organizacional

[INICIAR_LISTA_NUMERICA]
Primeiro item
Segundo item
[FINALIZAR_LISTA_NUMERICA]

2.1 Indicadores

Tabela Justiça em Números

Meta 1

Meta 2

3. CONCLUSÕES
...
```

### Configuração de Caminhos

Edite `src/config.py`:
```python
FILENAME_WORD_SOURCE = "Conteudo_Fonte.docx"
FILENAME_PDF_SOURCE = "justica-em-numeros-2025.pdf"
FILENAME_EXCEL_SOURCE = "Informações TJMG_ASPLAG resposta do CEINFO.xlsx"

# Ou use caminhos completos
FILE_WORD_SOURCE = RAW_DIR / "seu_arquivo.docx"
```

---

## 💾 Estrutura de Dados Interna

### Mapa de Recursos Principal (`MAPA_RECURSOS`)

Localizado em `src/content/static_data.py`, mapeia cada recurso mencionado no Word para sua configuração:

```python
MAPA_RECURSOS = {
  # Tabelas Estáticas
  "Tabela Atos Normativos": {
    "tipo": "TABELA_ATOS",
    "dados": dados_tabela_atos,
    "titulo": "Tabela 01 - Atos Normativos..."
  },
  
  # Tabelas Dinâmicas (Leem dados do CSV)
  "Tabela Justiça em Números": {
    "tipo": "TABELA_JN_DINAMICA",
    "dados": None,  # Preenchido em tempo de execução
    "titulo": "Tabela 02 - Indicadores Judiciais"
  },
  
  # Metas CNJ (Leem de arquivo Excel)
  "Meta 1": {
    "tipo": "TABELA_METAS_DINAMICA",
    "titulo": "Meta 1 - Taxa de Congestionamento",
    "fonte_custom": "Dados: Conselho Nacional de Justiça"
  },
  
  # Imagens Canvas
  "Gráfico Estrutura": {
    "tipo": "IMAGEM",
    "arquivo": "estrutura.png",
    "fonte": "Processamento interno",
    "largura": 15.0,  # cm
    "recuo_esq": 0.5  # cm
  },
}
```

### Tipos de Dados por Módulo

| Módulo | Tipos de Dados | Formato |
|--------|---|---|
| jn_loader.py | Métricas judiciais (~100) | Dict{"chave": float/str} |
| cnj_loader.py | Indicadores tribunal (20+) | Dict{"metrica": valor formatado} |
| static_data.py | Tabelas hardcoded | List[Tuple[...]] |
| builders.py | Tabelas processadas | Document table object |
| images.py | Imagens carregadas | Picture object (python-docx) |

---

## 🧪 Testing

### Testes Existentes
```bash
# Testes de tabelas
python teste_tabelas.py

# Testes de extração Excel
python src/extractors/excel_loader.py

# Análise diagnóstica de PDF
python src/tools/diagnose_pdf.py
```

### Notebooks Exploratórios
- `Notebooks/tratamento.ipynb`: Processamento de metas, pivot tables, análise
- `Notebooks/gráficos.ipynb`: Visualizações e plots
- `Notebooks/graficos_2.ipynb`: Gráficos adicionais

---

## 📝 Exemplos de Saída

### Tabela Gerada (Excerpt)
```
┌──────────────────────────────┬────────────────────────────────────┐
│ Ato Normativo                │ Estrutura                          │
├──────────────────────────────┼────────────────────────────────────┤
│ Lei Complementar nº 59/2001  │ Contém a organização e a divisão  │
│                              │ judiciárias do Estado de MG        │
├──────────────────────────────┼────────────────────────────────────┤
│ Resolução nº 1128/2026       │ Dispõe sobre a estrutura...        │
│                              │ • Secretaria de Governança...      │
│                              │ • Gabinete da Presidência...       │
└──────────────────────────────┴────────────────────────────────────┘

Tabela 01 - Atos Normativos referentes à Estrutura do TJMG. Fonte: Portal TJMG
```

### Métricas Extraídas
```
Ano base: 2025
Nº de magistrados: 501
Força de trabalho: 5.120
Casos novos: 156.000
Taxa de congestionamento Total: 38,9%
Taxa de congestionamento líquida: 36,2%
IPM (Índice Produtividade Magistrados): 85,2
```

---

## 🔒 Segurança e Validação

### Validações Implementadas
- ✅ Verificação de existência de arquivos antes de processamento
- ✅ Tratamento de erros em parsing de CSV (on_bad_lines='skip')
- ✅ Fallbacks automáticos quando dados faltam
- ✅ Sanitização de nomes de arquivo (remove caracteres inválidos)
- ✅ Limites de largura de imagem (máx 16cm)

### Tratamento de Erros
```python
try:
    extrair_imagens()
except Exception as e:
    print(f"⚠️ Aviso: Falha na extração: {e}")
    print("O relatório tentará ser gerado com imagens estáticas apenas")
```

---

## 🚀 Roadmap e Melhorias Futuras

### Curto Prazo
- [ ] Suporte a mais formatos de imagem (SVG, TIFF)
- [ ] Cache de dados processados para performance
- [ ] Validação automática de integridade de documento gerado
- [ ] Testes unitários completos

### Médio Prazo
- [ ] Integração completa com JIRA (leitura de status de tarefas)
- [ ] API REST para geração sob demanda
- [ ] Dashboard interativo de métricas
- [ ] Versionamento automático de relatórios

### Longo Prazo
- [ ] Machine Learning para detecção de anomalias em dados
- [ ] Geração em múltiplos idiomas
- [ ] Suporte a PDF como output (além de DOCX)
- [ ] Web interface para configuração/execução

---

## 📞 Suporte e Documentação

### Estrutura de Logs
O projeto utiliza `logging` configurado em `src/core/generator.py`:
```python
logging.basicConfig(
  level=logging.INFO,
  format='%(asctime)s - %(levelname)s - %(message)s'
)
```

### Troubleshooting

| Problema | Causa | Solução |
|----------|-------|---------|
| "CSV não encontrado" | Caminho incorreto | Editar `src/config.py` FILE_*_SOURCE |
| "Imagem não extraída" | PDF corrompido | Usar `--extrair` force ou diagnostic tool |
| "Tabela malformada" | Dados não formatáveis | Validar entrada em dados_manuais.csv |
| "Encoding error" | Charset incorreto | CSV deve ser latin1, Excel UTF-8 |
| "Memory error" | PDF muito grande | Dividir extração em intervalos de página |

### Debug
```bash
# Ativa debug no terminal
python -c "import logging; logging.basicConfig(level=logging.DEBUG)" && python main.py

# Diagnóstico de PDF
python src/tools/diagnose_pdf.py

# Exploração de dados Excel
python src/tools/explorar_planilha.py
```

---

## 📄 Licença

[Inserir informação de licença conforme necessário]

---

## 👥 Contribuidores

- Desenvolvimento: TJMG / ASPLAG
- Últimas mudanças: Janeiro/2026

---

## 🔗 Links Úteis

- [Conselho Nacional de Justiça (CNJ)](https://cnj.jus.br)
- [Portal TJMG](https://www.tjmg.jus.br)
- [Relatório Justiça em Números](https://cnj.jus.br/programas-e-acoes/justica-em-numeros/)
- Documentação python-docx: https://python-docx.readthedocs.io/
- Documentação PyMuPDF: https://pymupdf.readthedocs.io/

---

**Última atualização:** Janeiro 2026  
**Versão:** 3.7 (Híbrido - Estático + Dinâmico)
