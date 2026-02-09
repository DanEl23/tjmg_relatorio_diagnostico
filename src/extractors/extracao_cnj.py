"""
Extrator de dados CNJ do PDF Justiça em Números.
Suporte a múltiplas cores de cinza e busca por texto.

Este módulo extrai imagens e dados do PDF do CNJ (Conselho Nacional de Justiça),
com capacidade de detectar legendas em diferentes tons de cinza e buscar
por padrões de texto específicos.
"""

import fitz  # PyMuPDF
import json
import re
import sys
import os
from pathlib import Path

# Ajuste de path para importação
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.config import (
    FILE_PDF_SOURCE, DIR_IMAGES_EXTRACTED, FILE_JSON_MAPPING, 
    Colors, Patterns
)


class GrayColorDetector:
    """
    Detector de cores cinza com suporte a múltiplos tons.
    
    Atributos:
        gray_ranges: Lista de intervalos de cores cinza aceitos
    """
    
    def __init__(self):
        """Inicializa o detector com intervalos padrão de cinza."""
        # Cores em cinza em formato decimal (0x000000 a 0xFFFFFF)
        # Cinza é quando R ≈ G ≈ B
        self.gray_ranges = [
            (0x000000, 0x404040),  # Cinza escuro/preto
            (0x404040, 0x808080),  # Cinza médio-escuro
            (0x808080, 0xBFBFBF),  # Cinza médio
            (0xBFBFBF, 0xE0E0E0),  # Cinza claro
        ]
        
    def is_gray(self, color_decimal):
        """
        Verifica se uma cor em decimal é cinza.
        
        Args:
            color_decimal: Cor em formato decimal (int)
            
        Returns:
            bool: True se a cor está em algum intervalo de cinza
        """
        # Converter decimal para RGB
        r = (color_decimal >> 16) & 0xFF
        g = (color_decimal >> 8) & 0xFF
        b = color_decimal & 0xFF
        
        # Verificar se é aproximadamente cinza (R ≈ G ≈ B)
        # Tolerância de 30 pontos entre os canais
        max_diff = max(abs(r-g), abs(r-b), abs(g-b))
        if max_diff > 30:
            return False
        
        # Verificar se está em algum intervalo definido
        for min_gray, max_gray in self.gray_ranges:
            if min_gray <= color_decimal <= max_gray:
                return True
        
        return False
    
    def add_gray_range(self, min_color, max_color):
        """
        Adiciona um novo intervalo de cinza.
        
        Args:
            min_color: Cor mínima em hex (ex: 0x808080)
            max_color: Cor máxima em hex (ex: 0xBFBFBF)
        """
        self.gray_ranges.append((min_color, max_color))


class TextSearcher:
    """
    Buscador de texto em PDF com suporte a padrões regex.
    """
    
    def __init__(self, patterns=None):
        """
        Inicializa o buscador de texto.
        
        Args:
            patterns: Lista de padrões regex ou None para usar padrões padrão
        """
        self.patterns = patterns or [
            # Padrão principal: aceita com ou sem descrição após o número
            r"^\s*(Figura|Gráfico|Quadro)\s+\d+(\s*[-–].*)?",
            # Padrão para tabelas
            r"^\s*(Tabela|Quadro)\s+\d+(\s*[-–].*)?",
        ]
    
    def search_text(self, text, pattern_index=0):
        """
        Busca por um padrão específico no texto.
        
        Args:
            text: Texto para buscar
            pattern_index: Índice do padrão a usar (default: 0)
            
        Returns:
            Match object ou None
        """
        if pattern_index >= len(self.patterns):
            return None
        
        return re.search(self.patterns[pattern_index], text, re.IGNORECASE)
    
    def search_all_patterns(self, text):
        """
        Busca por todos os padrões no texto.
        
        Args:
            text: Texto para buscar
            
        Returns:
            Lista de tuplas (pattern_index, match) para cada correspondência
        """
        matches = []
        for i, pattern in enumerate(self.patterns):
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                matches.append((i, match))
        
        return matches
    
    def add_pattern(self, pattern):
        """
        Adiciona um novo padrão de busca.
        
        Args:
            pattern: String regex do padrão
        """
        self.patterns.append(pattern)


def sanitizar_nome(nome):
    """
    Remove caracteres inválidos para nome de arquivo.
    
    Args:
        nome: Nome original
        
    Returns:
        str: Nome sanitizado
    """
    return re.sub(r'[\\/*?:"<>|]', "", nome).strip()


def extrair_imagens_cnj(
    color_filter=True,
    use_gray_detector=True,
    custom_patterns=None
):
    """
    Extrai imagens do PDF do CNJ com suporte a múltiplas cores de cinza
    e busca por texto.
    
    Args:
        color_filter: Se True, filtra por cores (verde ou cinza)
        use_gray_detector: Se True, usa detector de múltiplos tons de cinza
        custom_patterns: Lista de padrões regex customizados ou None
        
    Returns:
        dict: Mapeamento de gráficos extraídos
    """
    print(f"--- Iniciando Extração de Imagens CNJ do PDF ---")
    print(f"Fonte: {FILE_PDF_SOURCE}")
    print(f"Filtro de cor ativo: {color_filter}")
    print(f"Detector de cinza ativo: {use_gray_detector}")
    
    if not FILE_PDF_SOURCE.exists():
        print(f"❌ ERRO: Arquivo PDF não encontrado.")
        return {}

    # Garante que a pasta de destino esteja limpa ou criada
    DIR_IMAGES_EXTRACTED.mkdir(parents=True, exist_ok=True)
    
    # Inicializa detectores
    gray_detector = GrayColorDetector() if use_gray_detector else None
    text_searcher = TextSearcher(custom_patterns)
    
    doc = fitz.open(FILE_PDF_SOURCE)
    mapeamento_graficos = {}
    contador_imagens = 0
    
    # Estatísticas
    stats = {
        "total_pages": len(doc),
        "legendas_encontradas": 0,
        "legendas_verdes": 0,
        "legendas_cinza": 0,
        "legendas_outras": 0,
        "imagens_extraidas": 0
    }

    # Itera sobre as páginas
    for page_num, page in enumerate(doc):
        # Procura por texto que pareça legenda
        text_instances = page.get_text("dict")["blocks"]
        
        for block in text_instances:
            if "lines" not in block:
                continue
            
            for line in block["lines"]:
                for span in line["spans"]:
                    texto = span["text"].strip()
                    cor = span.get("color", 0)
                    
                    # Busca por padrões de legenda usando o text_searcher
                    matches = text_searcher.search_all_patterns(texto)
                    
                    if not matches:
                        continue
                    
                    stats["legendas_encontradas"] += 1
                    
                    # Verifica se a cor passa no filtro
                    if color_filter:
                        # Verifica se é verde (cor CNJ tradicional)
                        is_green = cor == Colors.PDF_LEGEND_GREEN
                        
                        # Verifica se é cinza (múltiplos tons)
                        is_gray = False
                        if gray_detector:
                            is_gray = gray_detector.is_gray(cor)
                        
                        # Se não é nem verde nem cinza, pula
                        if not is_green and not is_gray:
                            stats["legendas_outras"] += 1
                            continue
                        
                        if is_green:
                            stats["legendas_verdes"] += 1
                        elif is_gray:
                            stats["legendas_cinza"] += 1
                    
                    # Extrai o ID da legenda (ex: "Figura 01")
                    match_id = re.search(
                        r"((?:Figura|Gráfico|Quadro|Tabela)\s+\d+)", 
                        texto, 
                        re.IGNORECASE
                    )
                    
                    if match_id:
                        nome_legenda = match_id.group(1)
                    else:
                        nome_legenda = f"Imagem_Pag{page_num+1}"

                    nome_arquivo = f"{sanitizar_nome(nome_legenda)}.png"
                    caminho_completo = DIR_IMAGES_EXTRACTED / nome_arquivo
                    
                    # Define a área de recorte (Crop)
                    rect = page.rect
                    clip_rect = fitz.Rect(
                        rect.x0 + 30,                    # Margem Esq
                        max(0, span["bbox"][1] - 400),   # Topo (400px acima)
                        rect.x1 - 30,                    # Margem Dir
                        span["bbox"][1]                  # Base (legenda)
                    )
                    
                    # Realiza o recorte e salva
                    pix = page.get_pixmap(clip=clip_rect, dpi=150)
                    pix.save(str(caminho_completo))
                    
                    # Salva no dicionário
                    mapeamento_graficos[nome_legenda] = {
                        "pagina": page_num + 1,
                        "caminho_completo": str(caminho_completo),
                        "status": "encontrado",
                        "cor": f"#{cor:06x}",
                        "tipo_cor": "verde" if cor == Colors.PDF_LEGEND_GREEN else "cinza"
                    }
                    
                    print(f"✅ Extraído: {nome_arquivo} (Pág {page_num+1}, Cor: #{cor:06x})")
                    contador_imagens += 1
                    stats["imagens_extraidas"] += 1

    # Salva o JSON de mapeamento
    with open(FILE_JSON_MAPPING, 'w', encoding='utf-8') as f:
        json.dump(mapeamento_graficos, f, indent=4, ensure_ascii=False)
    
    # Exibe estatísticas
    print(f"\n--- Estatísticas de Extração ---")
    print(f"Total de páginas processadas: {stats['total_pages']}")
    print(f"Legendas encontradas: {stats['legendas_encontradas']}")
    print(f"  - Legendas verdes (CNJ): {stats['legendas_verdes']}")
    print(f"  - Legendas cinza: {stats['legendas_cinza']}")
    print(f"  - Legendas outras cores (ignoradas): {stats['legendas_outras']}")
    print(f"Imagens extraídas: {stats['imagens_extraidas']}")
    print(f"--- Concluído ---")
    print(f"Mapeamento salvo em: {FILE_JSON_MAPPING}")
    
    return mapeamento_graficos


if __name__ == "__main__":
    # Exemplo de uso com todas as funcionalidades
    print("="*70)
    print("EXTRATOR CNJ - Suporte a Múltiplas Cores de Cinza e Busca por Texto")
    print("="*70)
    print()
    
    # Executa extração com todas as funcionalidades habilitadas
    mapeamento = extrair_imagens_cnj(
        color_filter=True,           # Ativa filtro de cores
        use_gray_detector=True,      # Ativa detector de múltiplos tons de cinza
        custom_patterns=None         # Usa padrões padrão
    )
    
    print(f"\n✨ Extração concluída! {len(mapeamento)} imagens processadas.")
