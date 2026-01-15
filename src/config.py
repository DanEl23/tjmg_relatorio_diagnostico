# src/config.py
import os
from pathlib import Path

# =============================================================================
# 1. CAMINHOS DE DIRETÓRIOS E ARQUIVOS
# =============================================================================
# Define a raiz do projeto (sobe um nível a partir de 'src')
BASE_DIR = Path(__file__).resolve().parent.parent

# Estrutura de Pastas de Dados
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"             # Onde ficam os arquivos originais (PDF, Excel, Word Fonte)
PROCESSED_DIR = DATA_DIR / "processed" # Onde ficam imagens extraídas e jsons gerados
IMAGES_DIR = PROCESSED_DIR / "canvas_images"  # Imagens processadas para inclusão no relatório
OUTPUT_DIR = DATA_DIR / "output"       # Onde o relatório final será salvo
RESOURCES_DIR = BASE_DIR / "resources" # Imagens estáticas (capa, margens)

# Nomes de Arquivos de Entrada (Centralizados aqui para fácil alteração)
FILENAME_WORD_SOURCE = "Conteudo_Fonte.docx"
FILENAME_PDF_SOURCE = "justica-em-numeros-2025.pdf"
FILENAME_EXCEL_SOURCE = "Informações TJMG_ASPLAG resposta do CEINFO.xlsx"
FILENAME_JSON_MAPPING = "mapeamento_graficos_completo.json"
FILENAME_TEMPLATE = "Sumario_Modelo.docx"
FILENAME_CAPA = "capa_relatorio.png"

# Caminhos Completos (Automáticos)
FILE_WORD_SOURCE = RAW_DIR / FILENAME_WORD_SOURCE
FILE_PDF_SOURCE = RAW_DIR / FILENAME_PDF_SOURCE
FILE_EXCEL_SOURCE = RAW_DIR / FILENAME_EXCEL_SOURCE
FILE_JSON_MAPPING = PROCESSED_DIR / FILENAME_JSON_MAPPING
FILE_TEMPLATE = RAW_DIR / FILENAME_TEMPLATE
FILE_CAPA_IMAGEM = RESOURCES_DIR / FILENAME_CAPA
DIR_IMAGES_EXTRACTED = PROCESSED_DIR / "extracted_images"
DIR_CANVAS_IMAGES = PROCESSED_DIR / "canvas_images"

# Configurações Visuais Globais
LARGURA_MAXIMA_IMAGEM = 16.0 # cm
# =============================================================================
# 2. ESTILOS VISUAIS (TJMG & RELATÓRIO)
# =============================================================================
class Colors:
    """Códigos Hexadecimais usados nas tabelas e estilos."""
    # Cores Institucionais / Cabeçalhos
    TJMG_BLUE = "44546A"       # Azul escuro (Cabeçalhos principais)
    HEADER_GRAY = "7F7F7F"     # Cinza médio (Atos, Áreas)
    HEADER_LIGHT_GRAY = "D9D9D9" # Cinza claro (Sub-cabeçalhos)
    
    # Cores de Conteúdo
    ZEBRA_STRIPE = "EEEEEE"    # Fundo alternado de linhas
    TOTAL_ROW = "BFBFBF"       # Linha de totais
    WHITE = "FFFFFF"
    BLACK = "000000"
    
    # Cores de Fonte Especiais
    HEADING_RED = (162, 22, 18) # RGB para Títulos H1, H2, H3
    PDF_LEGEND_GREEN = 37509    # Cor decimal usada na extração do PDF (aprox #009285)

class Fonts:
    MAIN = "Calibri"
    COVER = "Bahnschrift SemiCondensed"
    DEFAULT_SIZE = 12
    H1_SIZE = 18
    H2_SIZE = 16
    H3_SIZE = 15.5
    TABLE_HEADER_SIZE = 12
    TABLE_DATA_SIZE = 11

# =============================================================================
# 3. CONFIGURAÇÕES TÉCNICAS DO WORD
# =============================================================================
class Layout:
    # Margens ABNT / TJMG (em cm)
    MARGIN_TOP = 3.0
    MARGIN_LEFT = 3.0
    MARGIN_RIGHT = 2.0
    MARGIN_BOTTOM = 2.0
    
    # Cabeçalho e Rodapé (em cm)
    HEADER_DISTANCE = 1.0
    FOOTER_DISTANCE = 1.25
    
    # Tabelas
    TABLE_WIDTH_TWIPS = 9922     # Aprox 17.5 cm
    MIN_ROW_HEIGHT_TWIPS = 340   # Aprox 0.6 cm

# =============================================================================
# 4. REGEX E PADRÕES
# =============================================================================
class Patterns:
    # Captura títulos como "1. INTRODUÇÃO" ou "3.10. TÓPICO"
    TITULO = r'^\s*(\d+(?:\.\d{1,2})*\.?)\s+([A-ZÁÀÂÃÉÊÍÓÔÕÚÇ].*)$'
    
    # Captura legendas de imagens
    LEGENDA = r'^(Figura|Gráfico)\s+\d+'
    
    # Regex interno para encontrar gráficos no PDF (ajuste conforme extract_images.py)
    PDF_GRAPH_LEGEND = r"^\s*(Figura|Gráfico|Quadro)\s+\d+\s*[-–].+"
    
# Garante que os diretórios existam ao importar este arquivo
def ensure_directories():
    for path in [RAW_DIR, PROCESSED_DIR, OUTPUT_DIR, DIR_IMAGES_EXTRACTED]:
        path.mkdir(parents=True, exist_ok=True)

# Executa criação ao importar
ensure_directories()