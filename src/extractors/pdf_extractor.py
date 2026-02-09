import fitz  # PyMuPDF
import json
import re
import sys
import os

# Ajuste de path para importação
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.config import (
    FILE_PDF_SOURCE, DIR_IMAGES_EXTRACTED, FILE_JSON_MAPPING, 
    Colors, Patterns
)

def sanitizar_nome(nome):
    """Remove caracteres inválidos para nome de arquivo."""
    return re.sub(r'[\\/*?:"<>|]', "", nome).strip()

def buscar_texto_por_cor(page, texto_pattern, cor_alvo=None, tolerancia=5000):
    """
    CORRIGIDO: Suporte a busca por texto com filtro de cor.
    
    Busca texto no PDF que corresponde ao padrão e opcionalmente filtra por cor.
    
    Args:
        page: Página do PDF (objeto fitz.Page)
        texto_pattern: Padrão regex para buscar
        cor_alvo: Cor decimal alvo para filtrar (ex: Colors.PDF_LEGEND_GREEN)
        tolerancia: Tolerância na comparação de cores (valores próximos)
        
    Returns:
        list: Lista de dicionários com texto, posição e cor encontrados
    """
    resultados = []
    text_instances = page.get_text("dict")["blocks"]
    
    for block in text_instances:
        if "lines" not in block:
            continue
            
        for line in block["lines"]:
            for span in line["spans"]:
                texto = span["text"].strip()
                
                # Verifica se o texto corresponde ao padrão
                if re.search(texto_pattern, texto, re.IGNORECASE):
                    cor_span = span.get("color", 0)
                    
                    # Se não há filtro de cor, aceita qualquer resultado
                    if cor_alvo is None:
                        resultados.append({
                            "texto": texto,
                            "bbox": span["bbox"],
                            "cor": cor_span,
                            "tamanho": span.get("size", 0)
                        })
                    # Se há filtro de cor, verifica proximidade
                    elif abs(cor_span - cor_alvo) <= tolerancia:
                        resultados.append({
                            "texto": texto,
                            "bbox": span["bbox"],
                            "cor": cor_span,
                            "tamanho": span.get("size", 0)
                        })
    
    return resultados

def buscar_texto_multiplas_cores(page, texto_pattern, cores_alvo=None, tolerancia=5000):
    """
    CORRIGIDO: Suporte a múltiplas cores de cinza na busca por texto.
    
    Busca texto que corresponde ao padrão e filtra por múltiplas cores possíveis.
    Útil para encontrar legendas que podem estar em diferentes tons de cinza.
    
    Args:
        page: Página do PDF (objeto fitz.Page)
        texto_pattern: Padrão regex para buscar
        cores_alvo: Lista de cores decimais para filtrar (pode incluir tons de cinza)
        tolerancia: Tolerância na comparação de cores
        
    Returns:
        list: Lista de dicionários com texto, posição e cor encontrados
    """
    if cores_alvo is None:
        # Se não especificado, busca sem filtro de cor
        return buscar_texto_por_cor(page, texto_pattern, None, tolerancia)
    
    resultados = []
    for cor in cores_alvo:
        resultados.extend(buscar_texto_por_cor(page, texto_pattern, cor, tolerancia))
    
    # Remove duplicatas baseado na posição do texto
    resultados_unicos = []
    posicoes_vistas = set()
    
    for resultado in resultados:
        bbox_key = tuple(resultado["bbox"])
        if bbox_key not in posicoes_vistas:
            posicoes_vistas.add(bbox_key)
            resultados_unicos.append(resultado)
    
    return resultados_unicos

def extrair_imagens(usar_filtro_cor=False, cores_legendas=None):
    """
    CORRIGIDO: Extração de imagens com suporte a busca por texto e filtro de cor.
    
    Args:
        usar_filtro_cor: Se True, aplica filtro de cor nas legendas encontradas
        cores_legendas: Lista de cores decimais para filtrar legendas (ex: [Colors.PDF_LEGEND_GREEN])
    """
    print(f"--- Iniciando Extração de Imagens do PDF ---")
    print(f"Fonte: {FILE_PDF_SOURCE}")
    
    if usar_filtro_cor and cores_legendas:
        print(f"🎨 Usando filtro de cor: {len(cores_legendas)} cores configuradas")
    
    if not FILE_PDF_SOURCE.exists():
        print(f"❌ ERRO: Arquivo PDF não encontrado.")
        return

    # Garante que a pasta de destino esteja limpa ou criada
    DIR_IMAGES_EXTRACTED.mkdir(parents=True, exist_ok=True)
    
    doc = fitz.open(FILE_PDF_SOURCE)
    mapeamento_graficos = {}
    contador_imagens = 0

    # Itera sobre as páginas
    for page_num, page in enumerate(doc):
        # CORRIGIDO: Usa a nova função de busca por texto com suporte a múltiplas cores
        if usar_filtro_cor and cores_legendas:
            # Busca com filtro de cor
            legendas_encontradas = buscar_texto_multiplas_cores(
                page, 
                Patterns.PDF_GRAPH_LEGEND, 
                cores_legendas
            )
        else:
            # Busca sem filtro de cor (comportamento original)
            legendas_encontradas = buscar_texto_por_cor(
                page, 
                Patterns.PDF_GRAPH_LEGEND, 
                None
            )
        
        # Processa cada legenda encontrada
        for legenda_info in legendas_encontradas:
            texto = legenda_info["texto"]
            span_bbox = legenda_info["bbox"]
            
            # Regex ajustado para pegar "Figura X - Descrição"
            match_id = re.search(r"((?:Figura|Gráfico|Quadro)\s+\d+)", texto, re.IGNORECASE)
            if match_id:
                nome_legenda = match_id.group(1) # Ex: Figura 01
            else:
                nome_legenda = "Imagem_Sem_ID"

            nome_arquivo = f"{sanitizar_nome(nome_legenda)}.png"
            caminho_completo = DIR_IMAGES_EXTRACTED / nome_arquivo
            
            # Define a área de recorte (Crop)
            # Lógica simplificada: Pega a região acima da legenda
            rect = page.rect
            clip_rect = fitz.Rect(
                rect.x0 + 30,       # Margem Esq
                max(0, span_bbox[1] - 400), # Topo (400px acima da legenda)
                rect.x1 - 30,       # Margem Dir
                span_bbox[1]        # Base (onde começa a legenda)
            )
            
            # Realiza o recorte e salva
            pix = page.get_pixmap(clip=clip_rect, dpi=150)
            pix.save(str(caminho_completo))
            
            # Salva no dicionário para o Generator usar depois
            mapeamento_graficos[nome_legenda] = {
                "pagina": page_num + 1,
                "caminho_completo": str(caminho_completo),
                "status": "encontrado",
                "cor_texto": legenda_info["cor"]  # Sempre inclui informação de cor
            }
            
            cor_info = f" (cor: {legenda_info['cor']})" if usar_filtro_cor else ""
            print(f"✅ Extraído: {nome_arquivo} (Pág {page_num+1}){cor_info}")
            contador_imagens += 1

    # Salva o JSON de mapeamento
    with open(FILE_JSON_MAPPING, 'w', encoding='utf-8') as f:
        json.dump(mapeamento_graficos, f, indent=4, ensure_ascii=False)
        
    print(f"--- Concluído: {contador_imagens} imagens extraídas. ---")
    print(f"Mapeamento salvo em: {FILE_JSON_MAPPING}")
    
    return mapeamento_graficos

if __name__ == "__main__":
    extrair_imagens()