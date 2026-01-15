import re
from pathlib import Path
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION


# --- IMPORTS DO PROJETO ---
from src.content import static_data 
from src.media import images
from src.tables import builders

# --- CONFIGURAÇÃO VISUAL ---
COR_VINHO = RGBColor(162, 22, 18)
COR_PRETO = RGBColor(0, 0, 0)

def configurar_layout_pagina(document):
    """ Configura A4 e Margens padrão TJMG """
    section = document.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(3.0)
    section.bottom_margin = Cm(2.0)
    section.left_margin = Cm(3.0)
    section.right_margin = Cm(2.0)

def configurar_estilos_tjmg(document):
    """ Define estilos Heading 1, 2, 3 com a cor Vinho """
    styles = document.styles
    
    def criar_ou_atualizar_estilo(nome, tamanho, recuo, espaco_antes):
        try:
            if nome in styles:
                s = styles[nome]
            else:
                return 

            s.font.name = 'Calibri'
            s.font.size = Pt(tamanho)
            s.font.bold = True
            s.font.color.rgb = COR_VINHO
            
            pf = s.paragraph_format
            pf.space_before = Pt(espaco_antes)
            pf.space_after = Pt(6)
            pf.left_indent = Cm(recuo)
        except: pass

    # --- ATUALIZAÇÃO DOS RECUOS ---
    # Heading 1: Recuo de 1.25 cm (Mantido)
    criar_ou_atualizar_estilo('Heading 1', 16, 1.25, 18)
    
    # Heading 2 e 3: SEM RECUO (Alinhado à margem padrão)
    criar_ou_atualizar_estilo('Heading 2', 14, 0.0, 12)
    criar_ou_atualizar_estilo('Heading 3', 12, 0.0, 12)

def inserir_capa(document, pasta_resources):
    """ Insere a imagem de capa se ela existir """
    caminho_capa = pasta_resources / "capa_relatorio.png"

    if caminho_capa.exists():
        print("🖼️ Inserindo Capa...")
        p = document.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run()
        run.add_picture(str(caminho_capa), width=Cm(21.0))
        document.add_section(WD_SECTION.NEW_PAGE)
    else:
        print(f"⚠️ Capa não encontrada em: {caminho_capa}")

def gerar_relatorio_completo(caminho_base_dummy, output_path, mapa_recursos=None):
    """ Gera o relatório DO ZERO (Blank Document). """
    print(f"--- 🚀 Iniciando Geração (Modo Zero-Base) ---")

    # 1. SETUP DE DIRETÓRIOS
    pasta_raiz = Path(caminho_base_dummy).parent.parent
    if "src" in str(pasta_raiz): pasta_raiz = pasta_raiz.parent
    
    caminho_conteudo = pasta_raiz / "data" / "processed" / "Conteudo_Fonte.docx"
    caminho_sumario = pasta_raiz / "data" / "processed" / "Sumario_Modelo.docx"
    pasta_resources = pasta_raiz / "resources"
    
    if not caminho_conteudo.exists():
        caminho_conteudo = Path(caminho_base_dummy).parent / "Conteudo_Fonte.docx"
        caminho_sumario = Path(caminho_base_dummy).parent / "Sumario_Modelo.docx"
        pasta_resources = Path(caminho_base_dummy).parent.parent.parent / "resources"
        print(f"Pasta_resources ajustada para: {pasta_resources}")

    print(f"📂 Fonte: {caminho_conteudo}")
    print(f"📂 Sumário: {caminho_sumario}")

    # 2. CRIAÇÃO DO DOCUMENTO
    doc_final = Document()
    configurar_layout_pagina(doc_final)
    configurar_estilos_tjmg(doc_final)

    # 3. CAPA
    inserir_capa(doc_final, pasta_resources)

    # 4. SUMÁRIO (Com ajustes de formatação e espaçamento)
    try:
        doc_sumario_orig = Document(caminho_sumario)
        print("📋 Gerando página de Sumário...")
        adicionar_pagina_sumario_visual(doc_final, doc_sumario_orig)
        doc_final.add_page_break()
    except Exception as e:
        print(f"⚠️ Erro ao ler Sumario_Modelo ({e}). Pulando sumário.")

    # 5. PROCESSAMENTO DO CONTEÚDO
    try:
        doc_fonte = Document(caminho_conteudo)
    except:
        print("❌ Erro fatal: Conteudo_Fonte.docx não encontrado."); return

    mapa = static_data.MAPA_RECURSOS
    
    print("--- Processando Texto ---")
    for para in doc_fonte.paragraphs:
        texto = para.text.strip()
        if not texto: continue
        
        # Filtro de segurança (Ignora sumário antigo no texto)
        if texto.upper() == "SUMÁRIO" or re.match(r'^\d+$', texto):
            continue

        # A. COMANDOS
        if "[QUEBRA_PAGINA]" in texto:
            doc_final.add_page_break()
            continue

        # B. RECURSOS VISUAIS
        if texto in mapa:
            processar_recurso(doc_final, texto, mapa[texto])
            continue

        # C. TÍTULOS (Headings)
        match = re.match(r'^(\d+(\.\d+)*)\.?\s+(.*)', texto)
        if match:
            num = match.group(1)
            txt = match.group(3).strip()
            nivel = num.count('.') + 1
            if nivel > 3: nivel = 3
            
            print(f"🔖 Título: {num} {txt}")
            h = doc_final.add_heading(f"{num} {txt}", level=nivel)
            if h.runs: 
                h.runs[0].font.color.rgb = COR_VINHO
                h.runs[0].font.name = 'Calibri'
            continue

        # D. TEXTO COMUM
        p = doc_final.add_paragraph(texto)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        
        # Formatação do texto padrão
        p.paragraph_format.line_spacing = 1.5  
        p.paragraph_format.space_after = Pt(10) 
        
        run = p.runs[0] if p.runs else p.add_run(texto)
        run.font.name = 'Calibri'
        run.font.size = Pt(11)
        run.font.color.rgb = COR_PRETO

    # 6. SALVAR
    try:
        doc_final.save(output_path)
        print(f"✅ Relatório salvo em: {output_path}")
    except Exception as e:
        print(f"❌ Erro ao salvar: {e}")

# --- HELPER DE RECURSOS ---
def processar_recurso(doc, chave, item):
    tipo = item["tipo"]
    dados = item.get("dados")
    print(f"⚡ Inserindo: {chave}")

    if tipo == "IMAGEM":
        images.adicionar_imagem(
            doc, item["arquivo"], titulo=chave, 
            fonte=item.get("fonte", "Própria"),
            largura_custom=item.get("largura"),
            recuo_esq=item.get("recuo_esq", 0)
        )
    elif "TABELA_ORCAMENTO" in tipo:
        builders.adicionar_tabela_orcamento(
            doc, titulo_vindo_do_word=chave, dados=dados, 
            numero_tabela=item.get("num", "09"),
            titulo_custom=item.get("titulo")
        )
    elif tipo == "TABELA_PROCESSOS":
        builders.adicionar_tabela_processos(doc, dados, texto_legenda=chave)
    elif tipo == "TABELA_ATOS":
        builders.adicionar_tabela_atos(doc, dados)
    elif tipo == "TABELA_AREAS":
        builders.adicionar_tabela_areas(doc, dados)
    elif tipo == "TABELA_ESTRUTURA":
        builders.adicionar_tabela_estrutura(doc, dados)
    elif tipo == "TABELA_COMARCAS":
        builders.adicionar_tabela_comarcas(doc, dados)
    elif tipo == "TABELA_NUCLEOS":
        builders.adicionar_tabela_nucleos(doc, dados)
    elif tipo == "TABELA_CIDADES":
        builders.adicionar_tabela_cidades(doc, dados)
    elif tipo == "TABELA_JUSTICA_NUMEROS":
        builders.adicionar_tabela_justica_numeros(doc, dados)
    elif tipo == "TABELA_GENERICA":
        builders.adicionar_tabela_generica(doc, chave, dados)
    
    doc.add_paragraph() 

# --- FUNÇÃO DO SUMÁRIO (MANTIDA COM FORMATAÇÃO ESPECÍFICA) ---
def adicionar_pagina_sumario_visual(doc, doc_orig):
    # Título SUMÁRIO
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT 
    run = p.add_run("SUMÁRIO")
    run.bold = True
    run.font.size = Pt(20)
    run.font.color.rgb = COR_VINHO
    run.font.name = 'Calibri'
    p.paragraph_format.space_after = Pt(24)

    for para in doc_orig.paragraphs:
        txt = para.text.strip()
        if not txt: continue
        match = re.match(r'^(\d+(\.\d+)*)\.?\s+(.*)', txt)
        if match:
            num = match.group(1)
            t = match.group(3).split('...')[0].strip()
            lvl = num.count('.') + 1
            
            p_item = doc.add_paragraph()
            
            # Recuos Específicos do Sumário
            if lvl == 1: indent = Cm(0)
            elif lvl == 2: indent = Cm(0.42)
            elif lvl == 3: indent = Cm(0.85)
            else: indent = Cm(0.85)
                
            p_item.paragraph_format.left_indent = indent
            p_item.paragraph_format.line_spacing = 1.5
            p_item.paragraph_format.space_before = Pt(6)
            p_item.paragraph_format.space_after = Pt(5)
            
            run = p_item.add_run(f"{num} {t.upper() if lvl==1 else t}")
            run.bold = True
            run.font.size = Pt(12)
            run.font.color.rgb = COR_PRETO
            run.font.name = 'Calibri'