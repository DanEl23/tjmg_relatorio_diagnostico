import re
from pathlib import Path
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION

# --- IMPORTS PARA PAGINAÇÃO/XML ---
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

# --- IMPORTS DO PROJETO ---
from src.content import static_data 
from src.media import images
from src.tables import builders

# --- CONFIGURAÇÃO VISUAL ---
COR_VINHO = RGBColor(162, 22, 18)
COR_PRETO = RGBColor(0, 0, 0)


def configurar_layout_pagina(document):
    """ Configura A4, Margens e Distâncias de Cabeçalho/Rodapé """
    section = document.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    
    # Margens da Página
    section.top_margin = Cm(3.0)
    section.bottom_margin = Cm(2.0)
    section.left_margin = Cm(3.0)
    section.right_margin = Cm(2.0)
    
    # Distâncias
    section.header_distance = Cm(1.0)
    section.footer_distance = Cm(1.25)


def adicionar_paginacao_rodape(document):
    """ 
    Insere numeração de página no rodapé (Alinhado à Direita).
    - Ordem: [Número da Página] -> [Parágrafo em Branco].
    - Fonte: Calibri 12
    - Espaçamento: 1.5 (linhas) e 6pt (antes/depois).
    """
    section = document.sections[0]
    footer = section.footer
    
    # 1. Configura o parágrafo do NÚMERO DA PÁGINA
    if footer.paragraphs:
        p_num = footer.paragraphs[0]
        p_num.text = "" 
    else:
        p_num = footer.add_paragraph()
        
    p_num.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_num.paragraph_format.line_spacing = 1.5
    p_num.paragraph_format.space_before = Pt(6)
    p_num.paragraph_format.space_after = Pt(6)

    # 2. Força o Estilo 'Footer'
    try:
        style = document.styles['Footer']
        style.font.name = 'Calibri'
        style.font.size = Pt(12)
        style.paragraph_format.line_spacing = 1.5
        p_num.style = style
    except KeyError:
        pass

    # 3. Cria o Run e o Campo PAGE
    run = p_num.add_run()
    run.font.name = 'Calibri'
    run.font.size = Pt(12)
    
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')

    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = "PAGE"

    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'separate')

    fldChar3 = OxmlElement('w:fldChar')
    fldChar3.set(qn('w:fldCharType'), 'end')

    run._element.append(fldChar1)
    run._element.append(instrText)
    run._element.append(fldChar2)
    run._element.append(fldChar3)

    # 4. Adiciona um parágrafo VAZIO DEPOIS
    p_vazio = footer.add_paragraph()
    p_vazio.text = ""
    p_vazio.paragraph_format.line_spacing = 1.5 
    p_vazio.paragraph_format.space_before = Pt(6)
    p_vazio.paragraph_format.space_after = Pt(6)


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

    # Heading 1: Tamanho 16, Recuo de 1.25 cm
    criar_ou_atualizar_estilo('Heading 1', 16, 1.25, 18)
    
    # Heading 2 e 3: Tamanho 16, Sem recuo
    criar_ou_atualizar_estilo('Heading 2', 16, 0.0, 12)
    criar_ou_atualizar_estilo('Heading 3', 16, 0.0, 12)


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


def adicionar_texto_com_negrito(paragrafo, texto, cor_rgb=RGBColor(0,0,0), tamanho=12):
    """
    Processa o texto procurando por trechos entre asteriscos (*texto*).
    Gera 'runs' separados para aplicar negrito apenas onde necessário.
    """
    # Regex que divide o texto mantendo os delimitadores
    # (\*[^*]+\*) -> Captura grupos que começam e terminam com *, sem * no meio
    partes = re.split(r'(\*[^*]+\*)', texto)
    
    for parte in partes:
        if not parte: continue # Pula strings vazias resultantes do split
        
        run = paragrafo.add_run()
        
        # Se for um trecho entre asteriscos (*negrito*)
        if parte.startswith('*') and parte.endswith('*') and len(parte) > 2:
            texto_limpo = parte[1:-1] # Remove os *
            run.text = texto_limpo
            run.bold = True
        else:
            # Texto comum
            run.text = parte
            run.bold = False
            
        # Aplica a formatação padrão (Fonte/Cor/Tamanho) em TODOS os pedaços
        run.font.name = 'Calibri'
        run.font.size = Pt(tamanho)
        run.font.color.rgb = cor_rgb


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

    print(f"📂 Fonte: {caminho_conteudo}")
    print(f"📂 Sumário: {caminho_sumario}")

    # 2. CRIAÇÃO DO DOCUMENTO
    doc_final = Document()
    configurar_layout_pagina(doc_final)
    configurar_estilos_tjmg(doc_final)
    
    # --- PAGINAÇÃO ---
    adicionar_paginacao_rodape(doc_final)

    # 3. CAPA
    inserir_capa(doc_final, pasta_resources)

    # 4. SUMÁRIO (Visual)
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
    
    # Variáveis de Estado
    em_lista_numerica = False
    em_lista_marcadores = False

    print("--- Processando Texto ---")
    for para in doc_fonte.paragraphs:
        texto = para.text.strip()
        if not texto: continue
        
        # --- FILTRO: LIXO DE SUMÁRIO ANTIGO ---
        if texto.upper() == "SUMÁRIO" or re.match(r'^\d+$', texto):
            continue

        # --- CONTROLE DE LISTAS ---
        if "[INICIAR_LISTA_NUMERICA]" in texto:
            em_lista_numerica = True; continue 
        if "[FINALIZAR_LISTA_NUMERICA]" in texto:
            em_lista_numerica = False
            if doc_final.paragraphs:
                doc_final.paragraphs[-1].paragraph_format.space_after = Pt(16)
            continue

        if "[INICIAR_LISTA_MARCADORES]" in texto:
            em_lista_marcadores = True; continue
        if "[FINALIZAR_LISTA_MARCADORES]" in texto:
            em_lista_marcadores = False
            if doc_final.paragraphs:
                doc_final.paragraphs[-1].paragraph_format.space_after = Pt(16)
            continue

        # --- A. TEXTO DESTAQUE (Iniciado por #) ---
        if texto.startswith('#'):
            texto_limpo = texto.lstrip('#').strip()
            if not texto_limpo: continue

            print(f"⭐ Texto Destaque: {texto_limpo}")
            p = doc_final.add_paragraph(texto_limpo)
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.line_spacing = 1.5
            p.paragraph_format.space_after = Pt(10)

            run = p.runs[0] if p.runs else p.add_run(texto_limpo)
            run.font.name = 'Calibri'
            run.font.size = Pt(12)
            run.bold = True
            run.font.color.rgb = COR_VINHO 
            continue

        # --- B. COMANDOS GERAIS ---
        if "[QUEBRA_PAGINA]" in texto:
            doc_final.add_page_break()
            continue

        # --- C. RECURSOS VISUAIS ---
        if texto in mapa:
            processar_recurso(doc_final, texto, mapa[texto])
            continue

        # --- D. TÍTULOS (Headings) ---
        match = re.match(r'^\s*(\d+(?:\.\d+)*\.?)\s+(.*)', texto)
        eh_titulo_valido = False
        
        if match:
            prefixo = match.group(1).strip()
            titulo_texto = match.group(2).strip()
            
            # Validação Rigorosa
            tem_ponto = '.' in prefixo
            segmentos = prefixo.replace('.', ' ').split()
            tem_numero_grande = any(len(seg) > 2 for seg in segmentos)
            
            if tem_ponto and not tem_numero_grande:
                eh_titulo_valido = True
                
                num_limpo = prefixo.rstrip('.')
                nivel = num_limpo.count('.') + 1
                if nivel > 3: nivel = 3
                
                if nivel == 1:
                    texto_final_titulo = f"{num_limpo}. {titulo_texto}"
                else:
                    texto_final_titulo = f"{num_limpo} {titulo_texto}"

                # Linha vazia antes do H2
                if nivel == 2:
                    doc_final.add_paragraph()

                print(f"🔖 Título Detectado: {texto_final_titulo}")
                h = doc_final.add_heading(texto_final_titulo, level=nivel)
                
                if h.runs: 
                    h.runs[0].font.color.rgb = COR_VINHO
                    h.runs[0].font.name = 'Calibri'
        
        if eh_titulo_valido:
            continue

        # --- E. TEXTO COMUM (OU ITEM DE LISTA) ---
        p = doc_final.add_paragraph() 
        
        if em_lista_numerica:
            try: p.style = 'List Number'
            except: pass 
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            
            p.paragraph_format.line_spacing = 1.0 
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.left_indent = Cm(1.27) 
            p.paragraph_format.first_line_indent = Cm(-0.63)
            
        elif em_lista_marcadores:
            try: p.style = 'List Bullet'
            except: pass
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            
            p.paragraph_format.line_spacing = 1.5 
            
            p.paragraph_format.left_indent = Cm(1.27)
            p.paragraph_format.first_line_indent = Cm(-0.63)

        else:
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.line_spacing = 1.5  
            p.paragraph_format.space_after = Pt(10) 
        
        # AQUI O TEXTO É INSERIDO PELA PRIMEIRA E ÚNICA VEZ
        adicionar_texto_com_negrito(p, texto, cor_rgb=COR_PRETO, tamanho=12)
        
    # 6. SALVAR
    try:
        doc_final.save(output_path)
        print(f"✅ Relatório salvo em: {output_path}")
    except Exception as e:
        print(f"❌ Erro ao salvar: {e}")

# --- HELPER DE RECURSOS ---
# --- HELPER DE RECURSOS ---
def processar_recurso(doc, chave, item):
    tipo = item["tipo"]
    dados = item.get("dados")
    
    # Tenta obter título e fonte customizados do dicionário (static_data.py)
    # Se não existirem, usa valores padrão
    titulo_real = item.get("titulo", chave) 
    fonte_custom = item.get("fonte_custom")

    print(f"⚡ Inserindo: {titulo_real}")

    # === IMAGENS ===
    if tipo == "IMAGEM":
        images.adicionar_imagem(
            doc, item["arquivo"], titulo=titulo_real, 
            fonte=item.get("fonte", "Própria"),
            largura_custom=item.get("largura"),
            recuo_esq=item.get("recuo_esq", 0)
        )
    
    # === TABELAS DE ORÇAMENTO ===
    elif tipo == "TABELA_ORCAMENTO_CONJUNTO":
        builders.adicionar_tabela_orcamento_conjunto(doc, dados)

    elif tipo == "TABELA_ORCAMENTO_CONJUNTO_COMPARACAO":
        builders.adicionar_tabela_orcamento_detalhada(doc, dados)
        
    elif tipo == "TABELA_ORCAMENTO":
        builders.adicionar_tabela_orcamento(
            doc, titulo_vindo_do_word=titulo_real, dados=dados, 
            numero_tabela=item.get("num", "09"),
            titulo_custom=item.get("titulo")
        )

    # === DEMAIS TABELAS ESPECÍFICAS ===
    elif tipo == "TABELA_PROCESSOS":
        builders.adicionar_tabela_processos(doc, dados, texto_legenda=titulo_real)
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
    
    # === TABELAS NOVAS ===
    elif tipo == "TABELA_CIDADES":
        builders.adicionar_tabela_cidades(doc, dados)
        
    elif tipo == "TABELA_JUSTICA_NUMEROS":
        builders.adicionar_tabela_justica_numeros(doc, dados, texto_legenda=titulo_real)

    # === GENÉRICA (AQUI ESTÁ A CORREÇÃO PRINCIPAL) ===
    elif tipo == "TABELA_GENERICA":
        # Agora passamos o 'titulo_real' e a 'fonte_custom' para o construtor
        builders.adicionar_tabela_generica(
            doc, 
            titulo_tabela=titulo_real, 
            dados=dados, 
            fonte=fonte_custom
        )
    
    if doc.paragraphs:
        doc.paragraphs[-1].paragraph_format.space_after = Pt(6)

# --- FUNÇÃO DO SUMÁRIO ---
def adicionar_pagina_sumario_visual(doc, doc_orig):
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