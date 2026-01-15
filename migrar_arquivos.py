import os
import shutil
from pathlib import Path

# --- CONFIGURAÇÃO DOS CAMINHOS ---

# Caminho da pasta ANTIGA (Origem)
# O 'r' antes das aspas é para o Python aceitar as barras invertidas do Windows
CAMINHO_ORIGEM = r"C:\Users\P0165559\Documents\Relatorios\Relatorio_Diagnostico - Copia"

# Caminho do NOVO projeto (Destino - pasta onde o script está rodando)
CAMINHO_DESTINO = Path.cwd()

# --- MAPEAMENTO DE MIGRAÇÃO ---
# Formato: "Nome do arquivo na pasta antiga": "Caminho/Nome no novo projeto"

ARQUIVOS_PARA_MIGRAR = {
    # 1. CORE (Lógica Principal)
    "report_generator_test.py": "src/core/generator.py",
    
    # 2. DADOS ESTÁTICOS (Conteúdo Hardcoded)
    "report_data.py": "src/content/static_data.py",
    
    # 3. EXTRATORES (Scripts que leem fontes externas)
    "extract_images.py": "src/extractors/pdf_extractor.py",
    "resultado_tjmg.py": "src/extractors/excel_loader.py",
    "extrair_tabela_processos.py": "src/extractors/process_extractor.py",
    
    # 4. UTILS & HELPERS
    "match_graficos.py": "src/utils/image_matcher.py",
    
    # 5. FERRAMENTAS (Tools de diagnóstico - Mantemos o nome original)
    "diagnostico_metadados.py": "src/tools/diagnostico_metadados.py",
    "diagnose_pdf.py": "src/tools/diagnose_pdf.py",
    "explorar_planilha.py": "src/tools/explorar_planilha.py",
    "extract_pdf_pages.py": "src/tools/extract_pdf_pages.py",
    
    # 6. DADOS BRUTOS (Arquivos de entrada)
    "Conteudo_Fonte.docx": "data/raw/Conteudo_Fonte.docx",
    "Sumario_Modelo.docx": "data/raw/Sumario_Modelo.docx",
    "Informações TJMG_ASPLAG resposta do CEINFO.xlsx": "data/raw/Informações TJMG_ASPLAG resposta do CEINFO.xlsx",
    # Nota: O PDF as vezes fica na raiz ou em export, o script tentará achar
    "justica-em-numeros-2025.pdf": "data/raw/justica-em-numeros-2025.pdf",
    
    # 7. METADADOS PROCESSADOS
    "mapeamento_graficos_completo.json": "data/processed/mapeamento_graficos_completo.json",
    "dicionario_graficos.json": "data/processed/dicionario_graficos.json",
    
    # 8. RESOURCES (Imagens estáticas)
    "resources/capa_relatorio.png": "resources/capa_relatorio.png",
    "resources/margem_final.png": "resources/margem_final.png",
}

# SCRIPTS DE TESTE (Para referência futura em src/staging)
SCRIPTS_TESTE = [
    "teste_tabela.py", "teste_tabela_areas.py", "teste_tabela_comarcas.py",
    "teste_tabela_estrutura.py", "teste_tabela_historicos.py", "teste_tabela_nucleos.py",
    "teste_tabela_orcamento.py", "teste_tabela_justica_numeros.py",
    "teste_busca_graficos.py", "extrair_tabelas_planilha.py"
]

def migrar():
    origem_base = Path(CAMINHO_ORIGEM)
    
    print(f"--- INICIANDO MIGRAÇÃO ---")
    print(f"DE:   {origem_base}")
    print(f"PARA: {CAMINHO_DESTINO}")
    
    if not origem_base.exists():
        print(f"❌ ERRO CRÍTICO: A pasta de origem não existe: {origem_base}")
        return

    # 1. Migrar Arquivos Mapeados
    print("\n>>> Copiando Arquivos Principais...")
    for arquivo_antigo, caminho_novo_str in ARQUIVOS_PARA_MIGRAR.items():
        # Tenta achar o arquivo na raiz da origem
        src_file = origem_base / arquivo_antigo
        
        # Se não achar e for o PDF, tenta procurar na pasta export da origem
        if not src_file.exists() and arquivo_antigo.endswith(".pdf"):
             src_file = origem_base / "export" / arquivo_antigo

        dst_file = CAMINHO_DESTINO / caminho_novo_str
        
        if src_file.exists():
            # Garante que a pasta de destino existe
            dst_file.parent.mkdir(parents=True, exist_ok=True)
            try:
                shutil.copy2(src_file, dst_file)
                print(f"✅ [OK] {arquivo_antigo} -> {caminho_novo_str}")
            except Exception as e:
                print(f"❌ [ERRO] Falha ao copiar {arquivo_antigo}: {e}")
        else:
            print(f"⚠️  [AVISO] Arquivo não encontrado na origem: {arquivo_antigo}")

    # 2. Migrar Scripts de Teste (Staging)
    print("\n>>> Copiando Scripts de Teste para Staging...")
    staging_dir = CAMINHO_DESTINO / "src/staging"
    staging_dir.mkdir(parents=True, exist_ok=True)
    
    for script in SCRIPTS_TESTE:
        src_file = origem_base / script
        dst_file = staging_dir / script
        
        if src_file.exists():
            shutil.copy2(src_file, dst_file)
            print(f"✅ [OK] {script} -> src/staging/")
        else:
            # Tenta procurar dentro de 'codigos teste' na origem
            src_file_alt = origem_base / "codigos teste" / script
            if src_file_alt.exists():
                shutil.copy2(src_file_alt, dst_file)
                print(f"✅ [OK] {script} (de codigos teste) -> src/staging/")

    # 3. Migrar Imagens Extraídas (Se houver)
    print("\n>>> Verificando Imagens Extraídas (canvas_images)...")
    origem_imgs = origem_base / "canvas_images"
    destino_imgs = CAMINHO_DESTINO / "data/processed/extracted_images"
    
    if origem_imgs.exists():
        destino_imgs.mkdir(parents=True, exist_ok=True)
        count = 0
        for item in origem_imgs.iterdir():
            if item.is_file():
                shutil.copy2(item, destino_imgs / item.name)
                count += 1
        print(f"✅ {count} imagens copiadas para data/processed/extracted_images")
    else:
        print("ℹ️  Pasta 'canvas_images' não encontrada na origem (sem problemas).")

    print("\n--- MIGRAÇÃO CONCLUÍDA ---")
    print("Verifique se os arquivos apareceram nas pastas 'src' e 'data' do novo projeto.")

if __name__ == "__main__":
    migrar()