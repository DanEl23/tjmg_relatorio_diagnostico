from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.shared import OxmlElement
from docx.oxml.ns import qn

# Importa as ferramentas que acabamos de criar
from .utils import (
    set_cell_vertical_alignment, set_row_height_at_least, 
    set_row_height_flexible, set_cell_bottom_border, set_group_top_border, 
    set_cell_all_borders, remove_all_borders, limpar_espacamento_lista
)


def adicionar_tabela_atos(document, dados):
    """ 
    Tabela 01: Atos Normativos 
    Fidelidade Visual: Ajuste fino de espaçamentos (0pt antes, 1.15 entrelinhas no header).
    """
    
    # --- Parâmetros ---
    COR_CABECALHO_HEX = '7F7F7F'                  
    COR_CINZA_CLARO_HEX = 'EEEEEE'                 
    COR_BRANCO_RGB = RGBColor(255, 255, 255)       
    COR_PRETO_RGB = RGBColor(0, 0, 0) 
    
    TAMANHO_FONTE_PADRAO = Pt(12) 
    FONTE = 'Calibri'
    
    # Alturas (Twips)
    ALTURA_HEADER_TWIPS = 397
    ALTURA_DADOS_TWIPS = 227 
    
    # Larguras
    LARGURA_TABELA_TWIPS = '9922' 
    COL_WIDTHS_TWIPS = [2700, 7222]

    # --- Criação ---
    table = document.add_table(rows=1, cols=len(dados[0]))
    
    try: table.style = 'Table Grid'
    except KeyError: pass
        
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # XML: Largura da Tabela
    tbl = table._tbl
    tblPr = tbl.tblPr
    if tblPr is None:
        tblPr = OxmlElement('w:tblPr')
        tbl.insert(0, tblPr)
    
    tblW = tblPr.find(qn('w:tblW'))
    if tblW is not None: tblPr.remove(tblW)
    tblW = OxmlElement('w:tblW')
    tblW.set(qn('w:w'), LARGURA_TABELA_TWIPS)
    tblW.set(qn('w:type'), 'dxa')
    tblPr.append(tblW)
    
    for i, row_data in enumerate(dados):
        row = table.add_row() if i > 0 else table.rows[0]
        
        # XML: Altura da Linha
        tr = row._tr
        trPr = tr.get_or_add_trPr()
        for existing in trPr.findall(qn('w:trHeight')): trPr.remove(existing)
            
        trHeight = OxmlElement('w:trHeight')
        val_altura = str(ALTURA_HEADER_TWIPS) if i == 0 else str(ALTURA_DADOS_TWIPS)
        trHeight.set(qn('w:val'), val_altura)
        trHeight.set(qn('w:hRule'), 'atLeast')
        trPr.append(trHeight)
            
        if i == 0: trPr.append(OxmlElement('w:tblHeader'))
        else:
            cantSplit = OxmlElement('w:cantSplit')
            cantSplit.set(qn('w:val'), '0')
            trPr.append(cantSplit)
            
        for j, cell_data in enumerate(row_data):
            cell = row.cells[j]
            
            # XML: Largura da Coluna
            tcPr = cell._element.get_or_add_tcPr()
            tcW = OxmlElement('w:tcW')
            tcW.set(qn('w:w'), str(COL_WIDTHS_TWIPS[j]))
            tcW.set(qn('w:type'), 'dxa')
            tcPr.append(tcW)
            
            set_cell_vertical_alignment(cell, 'center') 
            cell.text = "" 
            
            lines = cell_data.split('\n')
            is_first_content_line = True

            for k, line in enumerate(lines):
                line = line.strip()
                if not line: continue 
                
                is_list_item = line.startswith('ü')
                
                if is_first_content_line:
                    current_paragraph = cell.paragraphs[0]
                    is_first_content_line = False
                else:
                    current_paragraph = cell.add_paragraph()

                # --- CORREÇÃO CRÍTICA 1: Espaçamento Antes (Space Before) ---
                # Força ZERO para anular herança do template
                current_paragraph.paragraph_format.space_before = Pt(0)

                text_to_insert = line.replace('ü', '').strip() if is_list_item else line
                run = current_paragraph.add_run(text_to_insert)

                # Formatação Específica por Tipo de Linha
                if is_list_item:
                    current_paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    estilo_aplicado = False
                    for nome_estilo in ['List Bullet', 'Marcadores', 'Parágrafo com marcadores']:
                        try:
                            current_paragraph.style = nome_estilo
                            estilo_aplicado = True
                            break
                        except KeyError: continue
                    if not estilo_aplicado: run.text = "• " + run.text

                    limpar_espacamento_lista(current_paragraph)
                    
                elif i == 0:
                    # --- CORREÇÃO CRÍTICA 2: Cabeçalho ---
                    current_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    current_paragraph.paragraph_format.space_after = Pt(0)
                    current_paragraph.paragraph_format.line_spacing = 1.15
                else:
                    # Dados Normais
                    current_paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    current_paragraph.paragraph_format.space_after = Pt(0)
                    current_paragraph.paragraph_format.line_spacing = 1.0
                
                run.font.name = FONTE
                run.font.size = TAMANHO_FONTE_PADRAO
                run.bold = (i == 0)
                run.font.color.rgb = COR_BRANCO_RGB if i == 0 else COR_PRETO_RGB
            
            # Sombreamento
            shading = OxmlElement('w:shd')
            shading.set(qn('w:fill'), COR_CABECALHO_HEX if i == 0 else (COR_CINZA_CLARO_HEX if i % 2 == 0 else 'auto'))
            if i == 0 or i % 2 == 0:
                 cell._tc.get_or_add_tcPr().append(shading)

    # Legenda
    p_titulo_tabela = document.add_paragraph(style='Normal')
    p_titulo_tabela.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_titulo_tabela.paragraph_format.space_before = Pt(6)
    p_titulo_tabela.paragraph_format.space_after = Pt(12)
    
    run_titulo = p_titulo_tabela.add_run("Tabela 01 - Atos Normativos referentes à Estrutura do TJMG. Fonte: Portal TJMG")
    run_titulo.bold = False 
    run_titulo.font.name = FONTE
    run_titulo.font.size = Pt(8)


def adicionar_tabela_areas(document, dados):
    """ 
    Tabela 02: Principais Áreas 
    Fidelidade Visual: SEM BORDAS (Visual limpo), apenas sombramento e linhas de grupo.
    """
    
    # --- Configurações Físicas ---
    LARGURA_COL1 = 8220  # ~14.5 cm
    LARGURA_COL2 = 1701  # ~3.0 cm
    LARGURA_TOTAL = LARGURA_COL1 + LARGURA_COL2
    ALTURA_LINHA = 227   # 0.4 cm
    
    FONTE_NOME = 'Calibri'
    FONTE_HEADER = Pt(12)
    FONTE_TAM = Pt(11)

    # Cria tabela sem estilo padrão de grade
    table = document.add_table(rows=0, cols=2)
    # Removemos a linha: table.style = 'Table Grid'
    
    # XML: Largura Fixa da Tabela
    tbl = table._tbl
    tblPr = tbl.tblPr
    if tblPr is None:
        tblPr = OxmlElement('w:tblPr')
        tbl.insert(0, tblPr)
    
    tblW = tblPr.find(qn('w:tblW'))
    if tblW is not None: tblPr.remove(tblW)
        
    tblW = OxmlElement('w:tblW')
    tblW.set(qn('w:w'), str(LARGURA_TOTAL))
    tblW.set(qn('w:type'), 'dxa')
    tblPr.append(tblW)
    
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    # --- Função Auxiliar Local: Remover Bordas ---
    def limpar_bordas(cell):
        tcPr = cell._element.get_or_add_tcPr()
        tcBorders = OxmlElement('w:tcBorders')
        for side in ['top', 'left', 'bottom', 'right']:
            border = OxmlElement(f'w:{side}')
            border.set(qn('w:val'), 'nil') # 'nil' remove a borda
            tcBorders.append(border)
        
        # Remove definições antigas e aplica a "sem borda"
        old_borders = tcPr.find(qn('w:tcBorders'))
        if old_borders is not None: tcPr.remove(old_borders)
        tcPr.append(tcBorders)

    # --- Função Auxiliar Local: Borda Superior Apenas (Para Grupos) ---
    def adicionar_borda_topo(cell):
        tcPr = cell._element.get_or_add_tcPr()
        tcBorders = OxmlElement('w:tcBorders')
        
        # Topo: Linha sólida preta
        top = OxmlElement('w:top')
        top.set(qn('w:val'), 'single')
        top.set(qn('w:sz'), '4') # Tamanho 1/2 pt
        top.set(qn('w:color'), '000000')
        tcBorders.append(top)
        
        # Outros lados: Sem borda
        for side in ['left', 'bottom', 'right']:
            border = OxmlElement(f'w:{side}')
            border.set(qn('w:val'), 'nil')
            tcBorders.append(border)

        old_borders = tcPr.find(qn('w:tcBorders'))
        if old_borders is not None: tcPr.remove(old_borders)
        tcPr.append(tcBorders)

    # --- Função Auxiliar Local: Largura ---
    def set_width(cell, width_twips):
        tcPr = cell._element.get_or_add_tcPr()
        tcW = tcPr.find(qn('w:tcW'))
        if tcW is not None: tcPr.remove(tcW)
        tcW = OxmlElement('w:tcW')
        tcW.set(qn('w:w'), str(width_twips))
        tcW.set(qn('w:type'), 'dxa')
        tcPr.append(tcW)

    data_row_index = 0 

    for i, row_data in enumerate(dados):
        tipo, col1, col2 = row_data
        row = table.add_row()
        
        # XML: Altura da Linha
        tr = row._tr
        trPr = tr.get_or_add_trPr()
        
        # Remove qualquer altura pré-existente
        for h in trPr.findall(qn('w:trHeight')): 
            trPr.remove(h)
            
        trHeight = OxmlElement('w:trHeight')
        
        # --- Lógica de Altura Diferenciada ---
        if i == 0 or tipo == "HEADER":
            # Altura do Header (ex: 600 twips para ser bem visível)
            trHeight.set(qn('w:val'), '397') 
        else:
            # Altura padrão para as demais linhas
            trHeight.set(qn('w:val'), str(ALTURA_LINHA))
            
        trHeight.set(qn('w:hRule'), 'atLeast')
        trPr.append(trHeight)
        
        # Header Repeater
        if tipo.startswith("HEADER"): 
            trPr.append(OxmlElement('w:tblHeader'))
        else: 
            trPr.append(OxmlElement('w:cantSplit'))
        
        c1, c2 = row.cells[0], row.cells[1]

        # 1. Limpa bordas de TUDO inicialmente
        limpar_bordas(c1)
        limpar_bordas(c2)

        # 2. Define larguras iniciais
        set_width(c1, LARGURA_COL1)
        set_width(c2, LARGURA_COL2)

        # --- Lógica de Conteúdo e Estilo ---
        
        # Caso 1: Cabeçalho Principal (DENOMINAÇÃO)
        if tipo == "HEADER_MAIN":
            c1.merge(c2)
            set_width(c1, LARGURA_TOTAL)
            
            # Fundo Cinza Escuro
            shading = OxmlElement('w:shd')
            shading.set(qn('w:fill'), '7F7F7F')
            c1._tc.get_or_add_tcPr().append(shading)
            
            c1.text = ""
            p = c1.paragraphs[0]
            run = p.add_run(col1)
            run.font.name = FONTE_NOME
            run.font.size = FONTE_HEADER
            run.font.color.rgb = RGBColor(255, 255, 255) # Texto Branco
            run.bold = True
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            
        # Caso 2: Subtítulos de Grupo (SUPERINTENDÊNCIA...)
        elif tipo == "HEADER_GROUP_SIGLA":
            for j, (cell, texto) in enumerate([(c1, col1), (c2, col2)]):
                # Fundo Cinza Claro
                shading = OxmlElement('w:shd')
                shading.set(qn('w:fill'), 'D9D9D9')
                cell._tc.get_or_add_tcPr().append(shading)
                
                # Borda Superior Preta (Importante!)
                adicionar_borda_topo(cell)
                
                cell.text = ""
                p = cell.paragraphs[0]
                run = p.add_run(texto)
                run.font.name = FONTE_NOME
                run.font.size = FONTE_TAM
                run.bold = True
                run.font.color.rgb = RGBColor(0, 0, 0) # Texto Preto
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT if j == 0 else WD_ALIGN_PARAGRAPH.CENTER

        # Caso 3: Subtítulo Mesclado
        elif tipo == "HEADER_GROUP_MERGED":
            c1.merge(c2)
            set_width(c1, LARGURA_TOTAL)
            
            shading = OxmlElement('w:shd')
            shading.set(qn('w:fill'), 'D9D9D9')
            c1._tc.get_or_add_tcPr().append(shading)
            
            adicionar_borda_topo(c1)
            
            c1.text = ""
            p = c1.paragraphs[0]
            run = p.add_run(col1)
            run.font.name = FONTE_NOME
            run.font.size = FONTE_TAM
            run.bold = True
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT

        # Caso 4: Dados Mesclados
        elif tipo == "DATA_MERGED":
            data_row_index += 1
            c1.merge(c2)
            set_width(c1, LARGURA_TOTAL)
            
            # Zebrado
            if data_row_index % 2 == 0:
                shading = OxmlElement('w:shd')
                shading.set(qn('w:fill'), 'EEEEEE')
                c1._tc.get_or_add_tcPr().append(shading)
                
            c1.text = ""
            p = c1.paragraphs[0]
            run = p.add_run(col1)
            run.font.name = FONTE_NOME
            run.font.size = FONTE_TAM
            run.bold = False
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT

        # Caso 5: Dados Divididos (Linhas normais)
        elif tipo == "DATA_SPLIT":
            data_row_index += 1
            cor_fundo = 'EEEEEE' if data_row_index % 2 == 0 else 'auto'
            
            for j, (cell, texto) in enumerate([(c1, col1), (c2, col2)]):
                if cor_fundo != 'auto':
                    shading = OxmlElement('w:shd')
                    shading.set(qn('w:fill'), cor_fundo)
                    cell._tc.get_or_add_tcPr().append(shading)
                
                cell.text = ""
                p = cell.paragraphs[0]
                run = p.add_run(texto)
                run.font.name = FONTE_NOME
                run.font.size = FONTE_TAM
                run.bold = False
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT if j == 0 else WD_ALIGN_PARAGRAPH.CENTER

        # --- RESET DE ESPAÇAMENTO ---
        for cell in row.cells:
            set_cell_vertical_alignment(cell, 'center')
            for p in cell.paragraphs:
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(0)
                p.paragraph_format.line_spacing = 1.0

    # Legenda
    p = document.add_paragraph(style='Normal')
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(12)
    run = p.add_run("Tabela 02 - Principais áreas da Secretaria do TJMG. Fonte: Portal TJMG")
    run.font.name = 'Calibri'
    run.font.size = Pt(8)

    
def adicionar_tabela_estrutura(document, dados):
    """ Tabela 03: Estrutura (1 Coluna) - Formatação Rigorosa """
    
    LARGURA_TOTAL = 9922 # ~17.5 cm
    FONTE_HEADER = Pt(12)
    FONTE_TAM = Pt(11)
    ALTURA_LINHA = 227
    
    table = document.add_table(rows=0, cols=1)
    
    # Configuração de Largura
    tbl = table._tbl
    tblPr = tbl.tblPr
    if tblPr is None:
        tblPr = OxmlElement('w:tblPr')
        tbl.insert(0, tblPr)
    tblW = OxmlElement('w:tblW')
    tblW.set(qn('w:w'), str(LARGURA_TOTAL))
    tblW.set(qn('w:type'), 'dxa')
    tblPr.append(tblW)
    
    primeiro_grupo_visto = False

    for i, row_data in enumerate(dados):
        tipo, texto = row_data

        # --- Lógica corrigida para o Respiro ---
        if tipo == "HEADER_GROUP_MERGED":
            if primeiro_grupo_visto:
                # Só entra aqui do SEGUNDO grupo em diante
                empty_row = table.add_row()
                trPr_empty = empty_row._tr.get_or_add_trPr()
                trH_empty = OxmlElement('w:trHeight')
                trH_empty.set(qn('w:val'), '15') 
                trH_empty.set(qn('w:hRule'), 'atLeast')
                trPr_empty.append(trH_empty)
                
                # Reset agressivo para a linha não "expandir"
                cell_e = empty_row.cells[0]
                p_e = cell_e.paragraphs[0]
                p_e.paragraph_format.space_before = Pt(0)
                p_e.paragraph_format.space_after = Pt(0)
                p_e.paragraph_format.line_spacing = 0.7
                # Força uma fonte minúscula para garantir altura 15
                run_e = p_e.add_run("")
                run_e.font.size = Pt(1)
                
                remove_all_borders(cell_e)
            else:
                # É o primeiro grupo que encontramos, não fazemos nada e marcamos como visto
                primeiro_grupo_visto = True

        row = table.add_row()
        
        # Altura Manual
        tr = row._tr
        trPr = tr.get_or_add_trPr()
        # Remove qualquer altura pré-existente
        for h in trPr.findall(qn('w:trHeight')): 
            trPr.remove(h)
            
        trHeight = OxmlElement('w:trHeight')
        
        # --- Lógica de Altura Diferenciada ---
        if i == 0 or tipo == "HEADER":
            # Altura do Header (ex: 600 twips para ser bem visível)
            trHeight.set(qn('w:val'), '397') 
        else:
            # Altura padrão para as demais linhas
            trHeight.set(qn('w:val'), str(ALTURA_LINHA))

        trHeight.set(qn('w:hRule'), 'atLeast')
        trPr.append(trHeight)
        
        cell = row.cells[0]
        
        # Largura da Célula
        tcPr = cell._element.get_or_add_tcPr()
        tcW = OxmlElement('w:tcW')
        tcW.set(qn('w:w'), str(LARGURA_TOTAL))
        tcW.set(qn('w:type'), 'dxa')
        tcPr.append(tcW)

        cell.text = texto
        set_cell_vertical_alignment(cell, 'center')

        # Garante que o parágrafo existe e acessamos o run
        p = cell.paragraphs[0]
        if not p.runs:
            p.add_run(texto)
        run = p.runs[0]
        
        if tipo == "HEADER_MAIN":
            shading = OxmlElement('w:shd')
            shading.set(qn('w:fill'), '7F7F7F')
            cell._tc.get_or_add_tcPr().append(shading)
            
            p = cell.paragraphs[0]
            p.runs[0].font.color.rgb = RGBColor(255,255,255)
            p.runs[0].bold = True
            p.runs[0].font.size = FONTE_HEADER
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            
        elif tipo == "HEADER_GROUP_MERGED":
            shading = OxmlElement('w:shd')
            shading.set(qn('w:fill'), 'D9D9D9')
            cell._tc.get_or_add_tcPr().append(shading)
            set_group_top_border(cell)
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT

            run.font.size = FONTE_TAM

        else:
            run.font.size = FONTE_TAM

        # --- RESET DE ESPAÇAMENTO ---
        for p in cell.paragraphs:
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.0

    # Legenda
    p = document.add_paragraph(style='Normal')
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(12)
    run = p.add_run("Tabela 03 - Estruturas para a Prestação Jurisdicional na Segunda Instância. Fonte: Portal TJMG")
    run.font.name = 'Calibri'
    run.font.size = Pt(8)


def adicionar_tabela_comarcas(document, dados):
    """ 
    Tabela 04: Comarcas Instaladas 
    Fidelidade: Dados alinhados à ESQUERDA, Sem Grades, Zebrado.
    """
    
    LARGURA_TOTAL = 9922 
    LARGURA_COL = int(LARGURA_TOTAL / 4) 
    ALTURA_LINHA = 227
    
    FONTE_NOME = 'Calibri'
    FONTE_HEADER = Pt(12)
    FONTE_TAM = Pt(11)

    table = document.add_table(rows=0, cols=4)
    
    # XML: Largura Fixa
    tbl = table._tbl
    tblPr = tbl.tblPr
    if tblPr is None:
        tblPr = OxmlElement('w:tblPr')
        tbl.insert(0, tblPr)
    
    tblW = tblPr.find(qn('w:tblW'))
    if tblW is not None: tblPr.remove(tblW)
    tblW = OxmlElement('w:tblW')
    tblW.set(qn('w:w'), str(LARGURA_TOTAL))
    tblW.set(qn('w:type'), 'dxa')
    tblPr.append(tblW)
    
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    # --- Helpers ---
    def limpar_bordas(cell):
        tcPr = cell._element.get_or_add_tcPr()
        tcBorders = OxmlElement('w:tcBorders')
        for side in ['top', 'left', 'bottom', 'right']:
            border = OxmlElement(f'w:{side}')
            border.set(qn('w:val'), 'nil') 
            tcBorders.append(border)
        old_borders = tcPr.find(qn('w:tcBorders'))
        if old_borders is not None: tcPr.remove(old_borders)
        tcPr.append(tcBorders)

    def set_width(cell, width_twips):
        tcPr = cell._element.get_or_add_tcPr()
        tcW = tcPr.find(qn('w:tcW'))
        if tcW is not None: tcPr.remove(tcW)
        tcW = OxmlElement('w:tcW')
        tcW.set(qn('w:w'), str(width_twips))
        tcW.set(qn('w:type'), 'dxa')
        tcPr.append(tcW)

    data_idx = 0
    
    for i, row_data in enumerate(dados):
        tipo = row_data[0]
        row = table.add_row()
        
        # XML: Altura da Linha
        tr = row._tr
        trPr = tr.get_or_add_trPr()
        for h in trPr.findall(qn('w:trHeight')): 
            trPr.remove(h)
        trHeight = OxmlElement('w:trHeight')
        if i == 0 or tipo == "HEADER":
            trHeight.set(qn('w:val'), '397') 
        else:
            trHeight.set(qn('w:val'), str(ALTURA_LINHA))
        trHeight.set(qn('w:hRule'), 'atLeast')
        trPr.append(trHeight)
        
        if tipo.startswith("HEADER"):
            trPr.append(OxmlElement('w:tblHeader'))
        else:
            trPr.append(OxmlElement('w:cantSplit'))

        for cell in row.cells:
            limpar_bordas(cell)
            set_width(cell, LARGURA_COL)
            
        # --- Lógica de Conteúdo ---
        
        if tipo == "HEADER_MERGE_4":
            cell = row.cells[0].merge(row.cells[3])
            set_width(cell, LARGURA_TOTAL)
            
            cell.text = ""
            p = cell.paragraphs[0]
            run = p.add_run(row_data[1])
            run.font.name = FONTE_NOME
            run.font.size = FONTE_HEADER
            run.font.color.rgb = RGBColor(255,255,255)
            run.bold = True
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            
            shading = OxmlElement('w:shd')
            shading.set(qn('w:fill'), '7F7F7F')
            cell._tc.get_or_add_tcPr().append(shading)
            
        elif tipo == "DATA_4_COL":
            data_idx += 1
            cor_fundo = 'D9D9D9' if data_idx % 2 != 0 else 'auto'
            
            for j in range(4):
                cell = row.cells[j]
                
                if cor_fundo != 'auto':
                    shading = OxmlElement('w:shd')
                    shading.set(qn('w:fill'), cor_fundo)
                    cell._tc.get_or_add_tcPr().append(shading)

                cell.text = ""
                p = cell.paragraphs[0]
                texto_celula = row_data[j+1] if (j+1) < len(row_data) else ""
                
                run = p.add_run(str(texto_celula))
                run.font.name = FONTE_NOME
                run.font.size = FONTE_TAM
                run.font.color.rgb = RGBColor(0,0,0)
                
                # --- CORREÇÃO: ALINHAMENTO À ESQUERDA ---
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT

        # --- RESET GLOBAL DE ESPAÇAMENTO ---
        for cell in row.cells:
            set_cell_vertical_alignment(cell, 'center')
            for p in cell.paragraphs:
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(0)
                p.paragraph_format.line_spacing = 1.0

    # Legenda
    p = document.add_paragraph(style='Normal')
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(12)
    run = p.add_run("Tabela 04 - Comarcas Instaladas. Fonte: Infoguia")
    run.font.name = 'Calibri'
    run.font.size = Pt(8)
            

def adicionar_tabela_nucleos(document, dados):
    """ 
    Tabela 05: Núcleos (1 Coluna) 
    Fidelidade: Sem grade, Cabeçalhos com borda superior, Espaçamento 0pt.
    """
    
    LARGURA_TOTAL = 9922 # ~17.5 cm
    ALTURA_LINHA = 227
    
    FONTE_NOME = 'Calibri'
    FONTE_TAM = Pt(11)
    
    table = document.add_table(rows=0, cols=1)
    
    # XML: Largura Fixa
    tbl = table._tbl
    tblPr = tbl.tblPr
    if tblPr is None:
        tblPr = OxmlElement('w:tblPr')
        tbl.insert(0, tblPr)
    tblW = tblPr.find(qn('w:tblW'))
    if tblW is not None: tblPr.remove(tblW)
    tblW = OxmlElement('w:tblW')
    tblW.set(qn('w:w'), str(LARGURA_TOTAL))
    tblW.set(qn('w:type'), 'dxa')
    tblPr.append(tblW)
    
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    # --- Helpers ---
    def limpar_bordas(cell):
        tcPr = cell._element.get_or_add_tcPr()
        tcBorders = OxmlElement('w:tcBorders')
        for side in ['top', 'left', 'bottom', 'right']:
            border = OxmlElement(f'w:{side}')
            border.set(qn('w:val'), 'nil')
            tcBorders.append(border)
        old = tcPr.find(qn('w:tcBorders'))
        if old is not None: tcPr.remove(old)
        tcPr.append(tcBorders)

    def adicionar_borda_topo(cell):
        tcPr = cell._element.get_or_add_tcPr()
        tcBorders = OxmlElement('w:tcBorders')
        top = OxmlElement('w:top')
        top.set(qn('w:val'), 'single')
        top.set(qn('w:sz'), '4')
        top.set(qn('w:color'), '000000')
        tcBorders.append(top)
        for side in ['left', 'bottom', 'right']:
            border = OxmlElement(f'w:{side}')
            border.set(qn('w:val'), 'nil')
            tcBorders.append(border)
        old = tcPr.find(qn('w:tcBorders'))
        if old is not None: tcPr.remove(old)
        tcPr.append(tcBorders)

    for row_data in dados:
        tipo, texto = row_data
        row = table.add_row()
        
        # Altura Manual
        tr = row._tr
        trPr = tr.get_or_add_trPr()
        for h in trPr.findall(qn('w:trHeight')): trPr.remove(h)
        trHeight = OxmlElement('w:trHeight')
        trHeight.set(qn('w:val'), str(ALTURA_LINHA))
        trHeight.set(qn('w:hRule'), 'atLeast')
        trPr.append(trHeight)
        
        cell = row.cells[0]
        limpar_bordas(cell)
        
        # XML: Largura da Célula
        tcPr = cell._element.get_or_add_tcPr()
        tcW = tcPr.find(qn('w:tcW'))
        if tcW is not None: tcPr.remove(tcW)
        tcW = OxmlElement('w:tcW')
        tcW.set(qn('w:w'), str(LARGURA_TOTAL))
        tcW.set(qn('w:type'), 'dxa')
        tcPr.append(tcW)

        # Lógica de Conteúdo
        cell.text = ""
        p = cell.paragraphs[0]
        run = p.add_run(texto)
        run.font.name = FONTE_NOME
        run.font.size = FONTE_TAM
        
        if tipo == "HEADER_GROUP_MERGED":
            shading = OxmlElement('w:shd')
            shading.set(qn('w:fill'), 'D9D9D9')
            cell._tc.get_or_add_tcPr().append(shading)
            
            adicionar_borda_topo(cell)
            run.bold = True
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            
        else:
            # Dados normais
            run.bold = False
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT

        # Reset Espaçamento
        set_cell_vertical_alignment(cell, 'center')
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0

    # Legenda
    p = document.add_paragraph(style='Normal')
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(12)
    run = p.add_run("Tabela 05 - Relação dos Núcleos de Justiça 4.0. Fonte: Infoguia")
    run.font.name = 'Calibri'
    run.font.size = Pt(8)


def adicionar_tabela_processos(document, dados, texto_legenda=None):
    """ 
    Tabelas 06, 07, 08 (Processos, Julgamentos, Acervo)
    Correções: 
    1. Anos: '2022.0' agora vira '2022' (não '20220').
    2. Coluna 1: Texto mantido (não vira '0').
    """
    NUM_COLUNAS = 7
    LARGURA_TOTAL = 9922  # 17.5 cm
    LARGURA_COL_1 = 2600 
    LARGURA_COL_RESTO = int((LARGURA_TOTAL - LARGURA_COL_1) / 6)
    
    H_HEADER = 320 
    ALTURA_LINHA_DADOS = 280 
    
    FONTE_NOME = 'Calibri'
    FONTE_TAM = Pt(12)
    ESPACAMENTO_LINHA = 1.15
    
    COR_TITULO_BG = '7F7F7F'      
    COR_SUB_BG = 'FFFFFF'         
    COR_ZEBRADO = 'D9D9D9'        
    COR_TOTAL_BG = 'D0CECE'       
    COR_DEST_HEADER = '44546A'    
    COR_DEST_DADOS = 'D5DCE4'     
    IDX_DESTAQUE = 5

    # --- FUNÇÕES DE LIMPEZA INTELIGENTE ---
    def converter_para_float(valor):
        """
        Converte valor para float de forma segura.
        1. Tenta conversão direta (para floats do Python: 2022.0 -> 2022.0)
        2. Se falhar, tenta formato BR (remove ponto milhar: 1.234,56 -> 1234.56)
        """
        if isinstance(valor, (int, float)):
            return float(valor)
        
        s = str(valor).strip()
        if not s: return 0.0
        
        try:
            # Tentativa 1: Float padrão (resolve '2022.0')
            return float(s)
        except ValueError:
            try:
                # Tentativa 2: Formato BR (resolve '1.234,56')
                clean_val = s.replace('.', '').replace(',', '.')
                return float(clean_val)
            except:
                return 0.0

    def formatar_brasileiro(valor, is_ano=False):
        if valor is None or str(valor).strip() == "": return ""
        try:
            float_val = converter_para_float(valor)
            
            # Se for ano (2000-2100), exibe sem separador
            if is_ano and (2000 <= float_val <= 2100):
                 return "{:.0f}".format(float_val)
            
            # Formatação BR padrão
            return "{:,.0f}".format(float_val).replace(",", ".")
        except: 
            return str(valor)

    # --- Pre-processamento ---
    novos_dados = []
    totais_colunas = [0.0] * 6 
    tem_total_no_input = any(d[0] == "TOTAL_ROW" for d in dados)

    for d in dados:
        tipo, vals = d[0], list(d[1:])
        if tipo == "DATA_ROW":
            for idx in range(1, 6):
                if idx < len(vals):
                    totais_colunas[idx] += converter_para_float(vals[idx])
            
            nums = [converter_para_float(v) for v in vals[1:6] if str(v).strip()]
            media = sum(nums) / 5 if nums else 0
            
            if len(vals) < 7: vals.append(media)
            else: vals[6] = media
            novos_dados.append([tipo] + vals)
        else:
            novos_dados.append(d)

    if not tem_total_no_input:
        linha_total = ["TOTAL_ROW", "Total"]
        for s in totais_colunas[1:]: linha_total.append(s)
        linha_total.append(sum(totais_colunas[1:]) / 5)
        novos_dados.append(linha_total)

    # --- Construção da Tabela ---
    table = document.add_table(rows=0, cols=NUM_COLUNAS)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    tbl = table._tbl
    tblPr = tbl.tblPr if tbl.tblPr is not None else OxmlElement('w:tblPr')
    
    tblW = OxmlElement('w:tblW')
    tblW.set(qn('w:w'), str(LARGURA_TOTAL))
    tblW.set(qn('w:type'), 'dxa')
    tblPr.append(tblW)

    data_row_count = 0
    for row_data in novos_dados:
        tipo, vals = row_data[0], row_data[1:]
        row = table.add_row()
        
        trPr = row._tr.get_or_add_trPr()
        trH = OxmlElement('w:trHeight')
        trH.set(qn('w:val'), str(H_HEADER if tipo in ["HEADER_MERGE", "SUB_HEADER"] else ALTURA_LINHA_DADOS))
        trH.set(qn('w:hRule'), 'atLeast'); trPr.append(trH)

        if tipo == "DATA_ROW": data_row_count += 1

        for j, cell in enumerate(row.cells):
            tcPr = cell._element.get_or_add_tcPr()
            
            tw = OxmlElement('w:tcW')
            tw.set(qn('w:w'), str(LARGURA_COL_1 if j == 0 else LARGURA_COL_RESTO))
            tw.set(qn('w:type'), 'dxa'); tcPr.append(tw)
            
            tcB = OxmlElement('w:tcBorders')
            for s in ['top', 'left', 'bottom', 'right']:
                b = OxmlElement(f'w:{s}'); b.set(qn('w:val'), 'nil'); tcB.append(b)
            tcPr.append(tcB)

            # --- Lógica de Preenchimento ---
            if tipo == "HEADER_MERGE" and j == 0:
                c = cell.merge(row.cells[6])
                c.text = str(vals[0]).upper()
                sh = OxmlElement('w:shd'); sh.set(qn('w:fill'), COR_TITULO_BG); c._tc.get_or_add_tcPr().append(sh)
                p = c.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                r = p.runs[0]; r.font.color.rgb = RGBColor(255,255,255); r.bold = True
            
            elif tipo == "SUB_HEADER":
                # --- CORREÇÃO: Coluna 0 é texto puro, Colunas 1-5 são anos ---
                if j == 0:
                    texto = str(vals[j]) # Mantém "Instância"
                elif j == 6:
                    texto = "Média"
                else:
                    texto = formatar_brasileiro(vals[j], is_ano=True)
                
                cell.text = texto
                p = cell.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                r = p.runs[0]; r.bold = True
                
                tcB_sub = cell._element.get_or_add_tcPr().find(qn('w:tcBorders'))
                bt = OxmlElement('w:bottom'); bt.set(qn('w:val'), 'single'); bt.set(qn('w:sz'), '6'); bt.set(qn('w:color'), '000000')
                tcB_sub.append(bt)
                
                bg = '44546A' if j == IDX_DESTAQUE else COR_SUB_BG
                if j == IDX_DESTAQUE: r.font.color.rgb = RGBColor(255,255,255)
                sh = OxmlElement('w:shd'); sh.set(qn('w:fill'), bg); cell._tc.get_or_add_tcPr().append(sh)

            elif tipo in ["DATA_ROW", "TOTAL_ROW"]:
                is_total = (tipo == "TOTAL_ROW")
                # Coluna 0 sempre texto, demais formata
                cell.text = formatar_brasileiro(vals[j]) if j > 0 else str(vals[j])
                
                p = cell.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER 
                r = p.runs[0]; r.bold = is_total
                
                if j == IDX_DESTAQUE: bg = COR_DEST_DADOS
                elif is_total: bg = COR_TOTAL_BG
                elif data_row_count % 2 == 0: bg = COR_ZEBRADO
                else: bg = 'FFFFFF'
                sh = OxmlElement('w:shd'); sh.set(qn('w:fill'), bg); cell._tc.get_or_add_tcPr().append(sh)

            set_cell_vertical_alignment(cell, 'center')
            for p in cell.paragraphs:
                p.paragraph_format.space_before = p.paragraph_format.space_after = Pt(0)
                p.paragraph_format.line_spacing = ESPACAMENTO_LINHA
                for r in p.runs: 
                    r.font.name = FONTE_NOME; r.font.size = FONTE_TAM
                    if tipo == "TOTAL_ROW": r.bold = True

    # --- Legenda ---
    p_leg = document.add_paragraph()
    p_leg.paragraph_format.space_before = Pt(6)
    
    titulo_dados = str(novos_dados[0][1]).upper()
    prefixo = "08"
    if "PROCESSOS" in titulo_dados: prefixo = "06"
    elif "JULGAMENTOS" in titulo_dados: prefixo = "07"
    
    texto_final = texto_legenda if texto_legenda else novos_dados[0][1]
    
    txt_leg = f"Tabela {prefixo} - {texto_final}. Fonte: Centro de Informações para a Gestão Institucional – CEINFO"
    r_leg = p_leg.add_run(txt_leg); r_leg.font.name = FONTE_NOME; r_leg.font.size = Pt(8)

    
def adicionar_tabela_orcamento(document, titulo_vindo_do_word, dados, numero_tabela="09", titulo_custom=None):
    """
    Tabela de Orçamento com Título Superior e Legenda Inferior distintos.
    - titulo_custom: Título que aparece ACIMA da tabela (ex: Unidade Orçamentária...).
    - titulo_vindo_do_word: Texto usado na LEGENDA (ex: Tabela 09 - Despesa...).
    """
    # --- Configurações Físicas ---
    LARGURA_TOTAL = 9922 
    LARGURA_COL_1 = 6500  
    LARGURA_COL_2 = LARGURA_TOTAL - LARGURA_COL_1
    ALTURA_LINHA = 340 
    FONTE_NOME = 'Calibri'; FONTE_TAM = Pt(12); ESPACAMENTO_LINHA = 1.15
    COR_HEADER_BG = '7F7F7F'; COR_TOTAL_BG = 'BFBFBF'; COR_DADOS_BG = 'FFFFFF'

    # --- 1. TÍTULO SUPERIOR (Vindo do static_data) ---
    if titulo_custom:
        p_top = document.add_paragraph()
        p_top.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_top = p_top.add_run(str(titulo_custom))
        run_top.font.name = FONTE_NOME
        run_top.font.size = Pt(12)
        run_top.bold = True
        p_top.paragraph_format.space_after = Pt(12)

    # --- 2. CONSTRUÇÃO DA TABELA ---
    table = document.add_table(rows=0, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl = table._tbl
    tblPr = tbl.tblPr if tbl.tblPr is not None else OxmlElement('w:tblPr')
    tblW = OxmlElement('w:tblW'); tblW.set(qn('w:w'), str(LARGURA_TOTAL)); tblW.set(qn('w:type'), 'dxa'); tblPr.append(tblW)

    # Helpers de formatação
    def converter_para_float(valor):
        if isinstance(valor, (int, float)): return float(valor)
        s = str(valor).strip().replace('R$', '').replace(' ', '')
        if not s or s == '-': return 0.0
        try: return float(s.replace('.', '').replace(',', '.'))
        except: return 0.0

    def formatar_moeda(valor):
        val_float = converter_para_float(valor)
        if val_float == 0: return "-"
        return "{:,.2f}".format(val_float).replace(",", "X").replace(".", ",").replace("X", ".")

    for i, row_data in enumerate(dados):
        tipo = row_data[0]
        vals = [str(row_data[1]), str(row_data[2])] # Pega colunas 1 e 2
        
        row = table.add_row()
        trPr = row._tr.get_or_add_trPr()
        trH = OxmlElement('w:trHeight'); trH.set(qn('w:val'), str(ALTURA_LINHA)); trH.set(qn('w:hRule'), 'atLeast'); trPr.append(trH)

        # Repetição de cabeçalho
        if i == 0 or tipo == "SUB_HEADER":
            trPr.append(OxmlElement('w:tblHeader'))

        if tipo == "GROUP_TITLE":
            cell = row.cells[0]; cell.merge(row.cells[1])
            cell.text = vals[0].upper()
            sh = OxmlElement('w:shd'); sh.set(qn('w:fill'), COR_HEADER_BG); cell._tc.get_or_add_tcPr().append(sh)
            p = cell.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.runs[0]; r.font.name = FONTE_NOME; r.font.size = FONTE_TAM; r.bold = True; r.font.color.rgb = RGBColor(255,255,255)
            # Bordas
            tcPr = cell._element.get_or_add_tcPr(); tcBorders = OxmlElement('w:tcBorders')
            for edge in ['top', 'left', 'bottom', 'right']:
                border = OxmlElement(f'w:{edge}'); border.set(qn('w:val'), 'single'); border.set(qn('w:sz'), '4'); border.set(qn('w:color'), '000000'); tcBorders.append(border)
            tcPr.append(tcBorders)
            continue 

        for j, cell in enumerate(row.cells):
            tcPr = cell._element.get_or_add_tcPr()
            tw = OxmlElement('w:tcW'); tw.set(qn('w:w'), str(LARGURA_COL_1 if j == 0 else LARGURA_COL_2)); tw.set(qn('w:type'), 'dxa'); tcPr.append(tw)
            
            tcBorders = OxmlElement('w:tcBorders')
            for edge in ['top', 'left', 'bottom', 'right']:
                border = OxmlElement(f'w:{edge}'); border.set(qn('w:val'), 'single'); border.set(qn('w:sz'), '4'); border.set(qn('w:color'), '000000'); tcBorders.append(border)
            tcPr.append(tcBorders)

            texto_f = vals[j]
            if tipo == "SUB_HEADER": texto_f = texto_f.upper()
            if j == 1 and tipo in ["DATA_ROW", "TOTAL_ROW"]: texto_f = formatar_moeda(vals[j])

            cell.text = texto_f
            p = cell.paragraphs[0]; r = p.runs[0] if p.runs else p.add_run(texto_f)
            
            bg = COR_DADOS_BG; is_bold = False; f_color = '000000'
            if tipo == "SUB_HEADER": bg = COR_HEADER_BG; is_bold = True; f_color = 'FFFFFF'
            elif tipo == "TOTAL_ROW": bg = COR_TOTAL_BG; is_bold = True
            
            sh = OxmlElement('w:shd'); sh.set(qn('w:fill'), bg); cell._tc.get_or_add_tcPr().append(sh)
            set_cell_vertical_alignment(cell, 'center')
            p.paragraph_format.space_before = p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = ESPACAMENTO_LINHA
            
            if j == 0 and tipo != "SUB_HEADER":
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT; p.paragraph_format.left_indent = Pt(6)
            else: p.alignment = WD_ALIGN_PARAGRAPH.CENTER

            r.font.name = FONTE_NOME; r.font.size = FONTE_TAM; r.bold = is_bold; r.font.color.rgb = RGBColor.from_string(f_color)

    # --- 3. LEGENDA INFERIOR (Vindo do Word + Fonte) ---
    p_leg = document.add_paragraph()
    p_leg.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_leg.paragraph_format.space_before = Pt(6)
    
    # Lógica de fonte baseada no número
    fonte_final = "Armazém de Informações - BO SIAFI/MG" if str(numero_tabela) == "09" else "LOA"
    
    # Monta a legenda: Tabela XX - Texto do Word. Fonte: YYY
    texto_legenda = f"{titulo_vindo_do_word.strip()}. Fonte: {fonte_final}"
    
    r_leg = p_leg.add_run(texto_legenda)
    r_leg.font.name = FONTE_NOME; r_leg.font.size = Pt(8)


def adicionar_tabela_orcamento_conjunto(document, dados):
    table = document.add_table(rows=0, cols=2)
    table.columns[0].width = Cm(9.6)
    table.columns[1].width = Cm(6.4)
    for row_data in dados:
        tipo = row_data[0]
        vals = row_data[1:3]
        row = table.add_row()
        set_row_height_at_least(row, 340)
        for j in range(2):
            cell = row.cells[j]
            remove_all_borders(cell)
            set_cell_vertical_alignment(cell, 'center')
            if tipo == "GROUP_TITLE":
                if j == 0:
                    cell.merge(row.cells[1])
                    cell.text = vals[0]
                    set_cell_all_borders(cell)
                    shading = OxmlElement('w:shd')
                    shading.set(qn('w:fill'), '7F7F7F')
                    cell._tc.get_or_add_tcPr().append(shading)
                    cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255,255,255)
                    cell.paragraphs[0].runs[0].bold = True
                    cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
                continue
            cell.text = vals[j]
            set_cell_all_borders(cell)
            if tipo == "TOTAL_ROW":
                cell.paragraphs[0].runs[0].bold = True
                shading = OxmlElement('w:shd')
                shading.set(qn('w:fill'), 'BFBFBF')
                cell._tc.get_or_add_tcPr().append(shading)
    document.add_paragraph("Tabela 11 - Orçamento 2025. Fonte: LOA", style='Caption').alignment = WD_ALIGN_PARAGRAPH.LEFT


def adicionar_tabela_cidades(document, dados):
    """ Tabela 12: Cidades (4 colunas zebradas) """
    table = document.add_table(rows=0, cols=4)
    tbl = table._tbl
    
    # CORREÇÃO DO WARNING AQUI
    tblPr = tbl.tblPr
    if tblPr is None:
        tblPr = OxmlElement('w:tblPr')
        tbl.insert(0, tblPr)
        
    tblInd = OxmlElement('w:tblInd')
    tblInd.set(qn('w:w'), str(int(Cm(1.27).twips)))
    tblInd.set(qn('w:type'), 'dxa')
    tblPr.append(tblInd)
    
    data_idx = 0
    for row_data in dados:
        tipo = row_data[0]
        row = table.add_row()
        set_row_height_flexible(row, 584)
        if tipo == "DATA_ROW": data_idx += 1
        
        for j in range(4):
            cell = row.cells[j]
            cell.text = row_data[j+1]
            set_cell_all_borders(cell)
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            
            if tipo == "DATA_ROW" and data_idx % 2 != 0:
                shading = OxmlElement('w:shd')
                shading.set(qn('w:fill'), 'D9D9D9')
                cell._tc.get_or_add_tcPr().append(shading)


def adicionar_tabela_justica_numeros(document, dados, texto_legenda=None):
    """ 
    Tabela 13: Justiça em Números 
    - Fonte: Calibri
    - Alinhamento Vertical: Centro
    - Espaçamento: 0pt
    """
    if not dados: return

    table = document.add_table(rows=0, cols=7)
    tbl = table._tbl
    
    # Configuração da Tabela (XML)
    tblPr = tbl.tblPr
    if tblPr is None:
        tblPr = OxmlElement('w:tblPr')
        tbl.insert(0, tblPr)
        
    tblLayout = OxmlElement('w:tblLayout')
    tblLayout.set(qn('w:type'), 'fixed')
    tblPr.append(tblLayout)
    
    tblInd = OxmlElement('w:tblInd')
    tblInd.set(qn('w:w'), str(int(Cm(-1.15).twips)))
    tblInd.set(qn('w:type'), 'dxa')
    tblPr.append(tblInd)
    
    tblGrid = OxmlElement('w:tblGrid')
    widths = [Cm(5.5)] + [Cm(2.25)]*6
    for w in widths:
        gc = OxmlElement('w:gridCol')
        gc.set(qn('w:w'), str(int(w.twips)))
        tblGrid.append(gc)
    tbl.insert(1, tblGrid)
    
    data_idx = 0
    for row_data in dados:
        tipo = row_data[0]
        vals = row_data[1:]
        row = table.add_row()
        set_row_height_flexible(row, 272)
        
        trPr = row._tr.get_or_add_trPr()
        trPr.append(OxmlElement('w:cantSplit'))
        if tipo.startswith("HEADER") or tipo.startswith("SUB"):
            trPr.append(OxmlElement('w:tblHeader'))
            
        # --- HEADER PRINCIPAL MESCLADO ---
        if tipo == "HEADER_MERGE":
            c = row.cells[0].merge(row.cells[6])
            c.text = vals[0]
            
            # Formatação
            set_cell_vertical_alignment(c, 'center') # <--- ALINHAMENTO VERTICAL
            shading = OxmlElement('w:shd')
            shading.set(qn('w:fill'), '44546A')
            c._tc.get_or_add_tcPr().append(shading)
            
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            
            if p.runs:
                run = p.runs[0]
                run.font.name = 'Calibri' # <--- FONTE CALIBRI
                run.font.size = Pt(11)
                run.font.color.rgb = RGBColor(255,255,255)
                run.bold = True
            
            remove_all_borders(c)

        # --- SUBTÍTULOS ---
        elif tipo in ["SUB_HEADER", "SUB_HEADER_SECONDARY"]:
            for j in range(7):
                c = row.cells[j]
                c.text = vals[j]
                
                set_cell_vertical_alignment(c, 'center') # <--- ALINHAMENTO VERTICAL
                shading = OxmlElement('w:shd')
                shading.set(qn('w:fill'), 'EEEEEE')
                c._tc.get_or_add_tcPr().append(shading)
                remove_all_borders(c)
                
                p = c.paragraphs[0]
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(0)
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j > 0 else WD_ALIGN_PARAGRAPH.LEFT

                if p.runs:
                    run = p.runs[0]
                    run.font.name = 'Calibri' # <--- FONTE CALIBRI
                    run.font.size = Pt(11)
                    run.bold = True
                
                if tipo == "SUB_HEADER_SECONDARY":
                    set_cell_bottom_border(c)
                    
        # --- DADOS ---
        elif tipo == "DATA_ROW":
            data_idx += 1
            for j in range(7):
                c = row.cells[j]
                c.text = vals[j]
                
                set_cell_vertical_alignment(c, 'center') # <--- ALINHAMENTO VERTICAL
                remove_all_borders(c)
                
                if data_idx % 2 != 0:
                    shading = OxmlElement('w:shd')
                    shading.set(qn('w:fill'), 'D9D9D9')
                    c._tc.get_or_add_tcPr().append(shading)
                
                p = c.paragraphs[0]
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(0)
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j > 0 else WD_ALIGN_PARAGRAPH.LEFT
                
                if p.runs:
                    run = p.runs[0]
                    run.font.name = 'Calibri' # <--- FONTE CALIBRI
                    run.font.size = Pt(11)

    # Legenda Dinâmica
    if texto_legenda:
        p_legenda = document.add_paragraph(texto_legenda, style='Caption')
        p_legenda.alignment = WD_ALIGN_PARAGRAPH.LEFT
    else:
        # Fallback caso não seja passado texto
        document.add_paragraph("Tabela 12 - Dados estatísticos do Relatório Justiça em Números. Fonte: CNJ", style='Caption')


def adicionar_tabela_generica(document, titulo_tabela, dados):
    """
    Tabela Genérica (2 colunas) - Layout Ajustado Final.
    - Correção: Listas de marcadores voltam a aparecer (respeitando o estilo Bullet).
    - Correção: Texto comum sem recuo (0cm).
    - Correção: Sem linhas em branco no topo da célula.
    """
    if not dados: return

    # --- Configurações Físicas ---
    LARGURA_TOTAL = 9922 
    LARGURA_COL_1 = int(LARGURA_TOTAL * 0.3)
    LARGURA_COL_2 = LARGURA_TOTAL - LARGURA_COL_1
    
    FONTE_NOME = 'Calibri'
    ESPACAMENTO_LINHA = 1.0  
    COR_HEADER_BG = '7F7F7F'

    # --- Tabela ---
    table = document.add_table(rows=0, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    tbl = table._tbl
    tblPr = tbl.tblPr if tbl.tblPr is not None else OxmlElement('w:tblPr')
    tblW = OxmlElement('w:tblW'); tblW.set(qn('w:w'), str(LARGURA_TOTAL)); tblW.set(qn('w:type'), 'dxa'); tblPr.append(tblW)

    for i, linha in enumerate(dados):
        row = table.add_row()
        trPr = row._tr.get_or_add_trPr()
        
        trH = OxmlElement('w:trHeight')
        trH.set(qn('w:val'), '340')
        trH.set(qn('w:hRule'), 'atLeast')
        trPr.append(trH)

        texto_col1 = str(linha[0])
        texto_col2 = str(linha[1])

        # --- CABEÇALHO ---
        eh_cabecalho = (i == 0)
        if eh_cabecalho:
            tblHeader = OxmlElement('w:tblHeader')
            trPr.append(tblHeader)
            texto_col1 = texto_col1.upper()
            texto_col2 = texto_col2.upper()

        vals = [texto_col1, texto_col2]
        
        for j, cell in enumerate(row.cells):
            tcPr = cell._element.get_or_add_tcPr()
            
            # Larguras
            tw = OxmlElement('w:tcW')
            tw.set(qn('w:w'), str(LARGURA_COL_1 if j == 0 else LARGURA_COL_2))
            tw.set(qn('w:type'), 'dxa')
            tcPr.append(tw)
            
            # Bordas
            tcBorders = OxmlElement('w:tcBorders')
            for edge in ['top', 'left', 'bottom', 'right']:
                border = OxmlElement(f'w:{edge}')
                border.set(qn('w:val'), 'single')
                border.set(qn('w:sz'), '4')
                border.set(qn('w:space'), '0')
                border.set(qn('w:color'), '000000')
                tcBorders.append(border)
            tcPr.append(tcBorders)
            
            set_cell_vertical_alignment(cell, 'center')

            # --- CONTEÚDO ---
            texto_base = vals[j]
            
            # CASO ESPECIAL: Marcador 'ü' na área de dados
            if not eh_cabecalho and "ü" in texto_base:
                cell.text = "" # Limpa conteúdo (sobra 1 parágrafo vazio)
                
                # Flag para usar o parágrafo vazio existente na primeira inserção
                primeiro_uso = True
                
                itens = texto_base.split('ü')
                
                for k, item in enumerate(itens):
                    item_limpo = item.strip()
                    if not item_limpo: continue 
                    
                    # Seleciona ou cria parágrafo
                    if primeiro_uso:
                        p_atual = cell.paragraphs[0]
                        primeiro_uso = False
                    else:
                        p_atual = cell.add_paragraph()
                    
                    p_atual.text = item_limpo
                    
                    # Lógica de Estilo
                    # Se k==0 e o texto original NÃO começava com ü, é o texto introdutório.
                    eh_intro = (k == 0 and not texto_base.strip().startswith("ü"))
                    
                    if eh_intro:
                         # Texto Normal (Intro): Força ZERO recuo
                         p_atual.style = None 
                         p_atual.paragraph_format.left_indent = Pt(0) 
                    else:
                         # Item de Lista: Usa estilo Bullet
                         # IMPORTANTE: Não forçar left_indent=0 aqui, senão a bolinha some
                         p_atual.style = 'List Bullet'
                    
                    p_atual.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    p_atual.paragraph_format.line_spacing = ESPACAMENTO_LINHA
                    p_atual.paragraph_format.space_before = Pt(0)
                    p_atual.paragraph_format.space_after = Pt(0)
                    
                    if p_atual.runs:
                        run = p_atual.runs[0]
                        run.font.name = FONTE_NOME
                        run.font.size = Pt(12)
                        run.font.color.rgb = RGBColor(0,0,0)
                        run.bold = False

            else:
                # --- TEXTO NORMAL (Sem marcadores) ---
                cell.text = texto_base
                p = cell.paragraphs[0]
                
                p.paragraph_format.line_spacing = ESPACAMENTO_LINHA
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(0)
                p.paragraph_format.left_indent = Pt(0) # Remove recuo padrão indesejado

                run = p.runs[0] if p.runs else p.add_run(texto_base)
                run.font.name = FONTE_NOME
                run.font.size = Pt(12)

                if eh_cabecalho:
                    sh = OxmlElement('w:shd')
                    sh.set(qn('w:fill'), COR_HEADER_BG)
                    cell._tc.get_or_add_tcPr().append(sh)
                    
                    run.bold = True
                    run.font.color.rgb = RGBColor(255,255,255)
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                else:
                    run.bold = False
                    run.font.color.rgb = RGBColor(0,0,0)
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT if j == 0 else WD_ALIGN_PARAGRAPH.LEFT

    # --- LEGENDA ---
    p_leg = document.add_paragraph()
    p_leg.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_leg.paragraph_format.space_before = Pt(6)
    
    fonte_texto = "CEINFO" if "Atos" in titulo_tabela else "TJMG"
    titulo_formatado = titulo_tabela.strip()
    if not titulo_formatado.endswith('.'): titulo_formatado += "."
    texto_legenda = f"{titulo_formatado} Fonte: {fonte_texto}"
    
    r_leg = p_leg.add_run(texto_legenda)
    r_leg.font.name = FONTE_NOME
    r_leg.font.size = Pt(8)