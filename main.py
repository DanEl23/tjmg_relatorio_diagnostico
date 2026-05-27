import sys
import argparse
from pathlib import Path

# --- 1. Configuração de Ambiente ---
# Adiciona o diretório atual ao path para garantir que 'src' seja encontrado
sys.path.append(str(Path(__file__).parent))

# --- 2. Imports da Nova Arquitetura ---
from src.config import BASE_DIR, PROCESSED_DIR, DIR_IMAGES_EXTRACTED
# Importamos o MAPA (Dicionário) e não mais a lista simples
from src.content.static_data import MAPA_RECURSOS 
from src.core.generator import gerar_relatorio_completo
from src.extractors.pdf_extractor import extrair_imagens

def main():
    # --- 3. Configuração de Argumentos (CLI) ---
    parser = argparse.ArgumentParser(description="Automação de Relatório Diagnóstico TJMG (Híbrido)")
    parser.add_argument("--extrair", action="store_true", help="Força a extração de gráficos do PDF.")
    parser.add_argument("--saida", type=str, default="Relatorio_Final_Completo.docx", help="Nome do arquivo final.")
    
    args = parser.parse_args()

    print("\n=== TJMG Report Automator: Modo Híbrido ===")
    
    # --- 4. Etapa de Extração (Gráficos Dinâmicos do PDF) ---
    # Verifica se já existem imagens extraídas na pasta
    tem_imagens = any(DIR_IMAGES_EXTRACTED.glob("*.png")) if DIR_IMAGES_EXTRACTED.exists() else False
    
    if args.extrair or not tem_imagens:
        print(">>> Iniciando extração de imagens do PDF...")
        try:
            extrair_imagens() 
        except Exception as e:
            print(f"AVISO: Falha na extração de imagens do PDF: {e}")
            print("    O relatório tentará ser gerado apenas com as imagens estáticas (Canvas).")
    else:
        print(">>> Pulando extração (Imagens do PDF já detectadas). Use --extrair para forçar.")

    # --- 5. Definição de Caminhos Finais ---
    # Template: Fica em data/raw/Sumario_Modelo.docx
    template_path = BASE_DIR / "data" / "raw" / "Sumario_Modelo.docx"
    
    # Output: Fica em data/output/NomeEscolhido.docx
    output_dir = PROCESSED_DIR.parent / "output"
    output_dir.mkdir(exist_ok=True) # Cria a pasta se não existir
    output_path = output_dir / args.saida

    # --- 6. Execução do Gerador (Passando o Mapa de Recursos) ---
    print(f">>> Lendo 'Conteudo_Fonte.docx' e gerando relatório em:\n    {output_path}...")
    
    try:
        gerar_relatorio_completo(
            caminho_base_dummy=template_path, # <--- MUDANÇA AQUI (Nome do argumento alterado)
            output_path=output_path,
            mapa_recursos=MAPA_RECURSOS
        )
    except Exception as e:
        print(f"\nERRO FATAL durante a geração: {e}")
        import traceback
        traceback.print_exc()

    print("\n=== Processo Finalizado ===")

if __name__ == "__main__":
    main()