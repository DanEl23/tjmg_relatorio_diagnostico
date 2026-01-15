import re
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

# --- IMPORTS ---
from src.content import static_data 
from src.media import images
from src.tables import builders

# --- CONFIGURAÇÃO VISUAL ---
COR_VINHO = RGBColor(162, 22, 18)
COR_PRETO = RGBColor(0, 0, 0)

def configurar_estilos_tjmg(document):
    """ Define os estilos dos Títulos (Headings) no padrão TJMG """
    styles = document.styles
    
    def setup_style(name, size, indent, space_before, space_after):
        try:
            s = styles[name]
            s.font.name = 'Calibri'
            s.font.size = Pt(size)
            s.font.bold = True
            s.font.color.rgb = COR_VINHO
            pf = s.paragraph_format
            pf.space_before = Pt(space_before)
            pf.space_after = Pt(space_after)
            pf.left_indent = Cm(indent)
        except KeyError: pass

    setup_style('Heading 1', 16, 0.0, 18, 12) 
    setup_style('Heading 2', 14, 0.5, 12, 6)
    setup_style('Heading 3', 12, 1.0, 12, 6)

def gerar_relatorio_completo(template_path, output_path, mapa_recursos=None):
    print(f"--- Iniciando Geração ---")

    try:
        doc_final = Document(template_path)
        caminho_sumario = template_path.parent / "Sumario_Modelo.docx"
        caminho_fonte = template_path.parent / "Conteudo_Fonte.docx"
        doc_fonte = Document(caminho_fonte)
        
        try: doc_sumario_orig = Document(caminho_sumario)
        except: doc_sumario_orig = None
    except Exception as e:
        print(f"❌ Erro ao abrir arquivos: {e}"); return

    # 1. Configurar Estilos
    configurar_estilos_tjmg(doc_final)

    # 2. Gerar Sumário Bonito
    if doc_sumario_orig:
        print("📋 Gerando página de Sumário Formatada...")
        adicionar_pagina_sumario_visual(doc_final, doc_sumario_orig)
        doc_final.add_page_break()

    # 3. Loop Principal com FILTRO DE DUPLICIDADE
    mapa = static_data.MAPA_RECURSOS.copy() if static_data.MAPA_RECURSOS else {}
    
    # CONTROLE DE ESTADO:
    # Se detectarmos "SUMÁRIO" no texto lido, ativamos o modo ignorar
    # até encontrarmos um título válido que NÃO pareça índice.
    ignorando_sumario = False 

    print("--- Processando Conteúdo ---")
    for i, para in enumerate(doc_fonte.paragraphs):
        texto_original = para.text
        chave = texto_original.strip()
        
        if not chave: continue 

        # --- LÓGICA DE FILTRO (IGNORAR SUMÁRIO ANTIGO) ---
        chave_upper = chave.upper()
        
        # Gatilho: Se achar a palavra SUMÁRIO sozinha, começa a ignorar
        if chave_upper == "SUMÁRIO":
            print(f"🚫 [Filtro] Ignorando linha de cabeçalho de sumário antigo: '{chave}'")
            ignorando_sumario = True
            continue

        if ignorando_sumario:
            # Se a linha parece item de sumário (termina com número ou tem pontinhos)
            # Regex: Texto...Numero ou Texto (tab) Numero
            if re.search(r'(\.{3,}|\t)\s*\d+$', chave):
                print(f"🚫 [Filtro] Ignorando item de índice antigo: '{chave[:20]}...'")
                continue
            
            # Se for apenas um número isolado (número de página solto)
            if re.match(r'^\d+$', chave):
                continue

            # Se chegamos aqui, pode ser o fim do sumário.
            # Vamos testar se é um Título Real (Ex: "1 INTRODUÇÃO" ou "3 PERFIL")
            # Se for título real, desligamos o modo ignorar.
            if re.match(r'^\d+(\.\d+)*\.?\s+[A-Za-z]', chave):
                print(f"✅ [Filtro] Fim do sumário detectado. Retomando em: '{chave}'")
                ignorando_sumario = False
            else:
                # Se não parece título nem item de índice, mas estamos no modo ignorar...
                # Por segurança, se for texto curto, ignoramos.
                if len(chave) < 100:
                    print(f"🚫 [Filtro] Ignorando linha suspeita no início: '{chave}'")
                    continue

        # --- A. COMANDOS ---
        if "[QUEBRA_PAGINA]" in chave:
            doc_final.add_page_break()
            continue

        # --- B. RECURSOS VISUAIS ---
        if chave in mapa:
            item = mapa[chave]
            processar_recurso_visual(doc_final, chave, item)
            continue

        # --- C. TÍTULOS (Headings) ---
        match_titulo = re.match(r'^(\d+(\.\d+)*)\.?\s+(.*)', chave)
        
        if match_titulo:
            # Se caiu aqui, é um título real e deve ser impresso
            numeracao = match_titulo.group(1)
            # Limpeza extra para tirar tabs ou pontinhos que sobraram do regex
            titulo_texto = match_titulo.group(3).split('\t')[0].replace('.', '').strip()
            
            nivel = numeracao.count('.') + 1
            if nivel > 3: nivel = 3
            
            # DEBUG: Para ver o que está sendo classificado como título
            print(f"🔖 Título Detectado (L{nivel}): {numeracao} {titulo_texto}")

            h = doc_final.add_heading(f"{numeracao} {titulo_texto}", level=nivel)
            if h.runs: h.runs[0].font.color.rgb = COR_VINHO
            continue

        # --- D. TEXTO COMUM ---
        p = doc_final.add_paragraph(chave)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(10)
        
        if p.runs:
            p.runs[0].font.name = 'Calibri'
            p.runs[0].font.size = Pt(11)
        else:
            run = p.add_run(chave)
            run.font.name = 'Calibri'
            run.font.size = Pt(11)

    try:
        doc_final.save(output_path)
        print(f"✅ Relatório salvo em: {output_path}")
    except Exception as e:
        print(f"❌ Erro ao salvar: {e}")

# --- FUNÇÕES AUXILIARES ---

def processar_recurso_visual(doc, chave, item):
    """ Centraliza a lógica de inserção """
    tipo = item["tipo"]
    dados = item.get("dados")
    
    print(f"⚡ Inserindo Recurso: {chave}")

    if tipo == "IMAGEM":
        images.adicionar_imagem(
            doc, item["arquivo"], titulo=chave, 
            fonte=item.get("fonte", "Própria"),
            largura_custom=item.get("largura"),
            recuo_esq=item.get("recuo_esq", 0)
        )
    
    elif tipo in ["TABELA_ORCAMENTO", "TABELA_ORCAMENTO_CONJUNTO"]:
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

def adicionar_pagina_sumario_visual(doc, doc_sumario_orig):
    """ Gera o sumário formatado """
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("SUMÁRIO")
    run.bold = True; run.font.size = Pt(14); run.font.name = 'Calibri'
    run.font.color.rgb = COR_VINHO
    p.paragraph_format.space_after = Pt(24)

    for para in doc_sumario_orig.paragraphs:
        texto = para.text.strip()
        if not texto: continue
        
        # Regex flexível para o modelo do sumário
        match = re.match(r'^(\d+(\.\d+)*)\.?\s+(.*)', texto)
        if match:
            num = match.group(1)
            txt = match.group(3).split('...')[0].strip() # Limpa pontinhos
            
            nivel = num.count('.') + 1
            
            p_item = doc.add_paragraph()
            indent = 0 if nivel == 1 else (0.5 * (nivel - 1))
            p_item.paragraph_format.left_indent = Cm(indent)
            p_item.paragraph_format.space_after = Pt(2)
            
            texto_final = f"{num} {txt.upper() if nivel == 1 else txt}"
            run_item = p_item.add_run(texto_final)
            run_item.bold = True
            run_item.font.color.rgb = COR_PRETO
            run_item.font.name = 'Calibri'
            run_item.font.size = Pt(11)