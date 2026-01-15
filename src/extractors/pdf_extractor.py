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

def extrair_imagens():
    print(f"--- Iniciando Extração de Imagens do PDF ---")
    print(f"Fonte: {FILE_PDF_SOURCE}")
    
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
        # Procura por texto que pareça legenda (Gráfico X ou Figura Y)
        text_instances = page.get_text("dict")["blocks"]
        
        for block in text_instances:
            if "lines" not in block: continue
            
            for line in block["lines"]:
                for span in line["spans"]:
                    texto = span["text"].strip()
                    
                    # Regex ajustado para pegar "Figura X - Descrição"
                    # O re.IGNORECASE é fundamental aqui
                    match = re.search(Patterns.PDF_GRAPH_LEGEND, texto, re.IGNORECASE)
                    
                    if match:
                        # Pega o tipo e o número (ex: Figura 01)
                        # O regex retorna o match completo. Vamos extrair o ID.
                        match_id = re.search(r"((?:Figura|Gráfico|Quadro)\s+\d+)", texto, re.IGNORECASE)
                        if match_id:
                            nome_legenda = match_id.group(1) # Ex: Figura 01
                        else:
                            nome_legenda = "Imagem_Sem_ID"

                        nome_arquivo = f"{sanitizar_nome(nome_legenda)}.png"
                        caminho_completo = DIR_IMAGES_EXTRACTED / nome_arquivo
                        
                        # Define a área de recorte (Crop)
                        # Lógica simplificada: Pega a região acima da legenda
                        # Você pode ajustar esses valores se as imagens estiverem cortadas erradas
                        rect = page.rect
                        clip_rect = fitz.Rect(
                            rect.x0 + 30,       # Margem Esq
                            max(0, span["bbox"][1] - 400), # Topo (400px acima da legenda)
                            rect.x1 - 30,       # Margem Dir
                            span["bbox"][1]     # Base (onde começa a legenda)
                        )
                        
                        # Realiza o recorte e salva
                        pix = page.get_pixmap(clip=clip_rect, dpi=150)
                        pix.save(str(caminho_completo))
                        
                        # Salva no dicionário para o Generator usar depois
                        mapeamento_graficos[nome_legenda] = {
                            "pagina": page_num + 1,
                            "caminho_completo": str(caminho_completo),
                            "status": "encontrado"
                        }
                        
                        print(f"✅ Extraído: {nome_arquivo} (Pág {page_num+1})")
                        contador_imagens += 1

    # Salva o JSON de mapeamento
    with open(FILE_JSON_MAPPING, 'w', encoding='utf-8') as f:
        json.dump(mapeamento_graficos, f, indent=4, ensure_ascii=False)
        
    print(f"--- Concluído: {contador_imagens} imagens extraídas. ---")
    print(f"Mapeamento salvo em: {FILE_JSON_MAPPING}")

if __name__ == "__main__":
    extrair_imagens()