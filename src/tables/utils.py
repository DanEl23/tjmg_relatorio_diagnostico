from docx.shared import Pt
from docx.oxml.shared import OxmlElement
from docx.oxml.ns import qn

def set_cell_vertical_alignment(cell, align):
    """Define o alinhamento vertical de uma célula."""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    vAlign = OxmlElement('w:vAlign')
    vAlign.set(qn('w:val'), align) 
    tcPr.append(vAlign)

def set_row_height_at_least(row, height_twips):
    """Define altura mínima obrigatória (0.6cm aprox)."""
    ALTURA_MINIMA_OBRIGATORIA = 340
    altura_final = max(height_twips, ALTURA_MINIMA_OBRIGATORIA)
    tr = row._tr
    trPr = tr.get_or_add_trPr()
    trHeight = OxmlElement('w:trHeight')
    trHeight.set(qn('w:val'), str(altura_final))
    trHeight.set(qn('w:hRule'), 'atLeast')
    for existing in trPr.findall(qn('w:trHeight')): trPr.remove(existing)
    trPr.append(trHeight)

def set_row_height_flexible(row, height_twips):
    tr = row._tr
    trPr = tr.get_or_add_trPr()
    trHeight = OxmlElement('w:trHeight')
    trHeight.set(qn('w:val'), str(height_twips))
    trHeight.set(qn('w:hRule'), 'atLeast')
    for existing in trPr.findall(qn('w:trHeight')): trPr.remove(existing)
    trPr.append(trHeight)

def set_cell_bottom_border(cell):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '4')
    bottom.set(qn('w:color'), '000000')
    tcBorders.append(bottom)
    tcPr.append(tcBorders)

def set_group_top_border(cell):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    top = OxmlElement('w:top')
    top.set(qn('w:val'), 'single')
    top.set(qn('w:sz'), '4')
    top.set(qn('w:color'), '000000')
    tcBorders.append(top)
    tcPr.append(tcBorders)

def set_cell_all_borders(cell):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for side in ['w:top', 'w:bottom', 'w:left', 'w:right']:
        border = OxmlElement(side)
        border.set(qn('w:val'), 'single')
        border.set(qn('w:sz'), '4')
        border.set(qn('w:color'), '000000')
        tcBorders.append(border)
    for existing in tcPr.findall(qn('w:tcBorders')): tcPr.remove(existing)
    tcPr.append(tcBorders)

def remove_all_borders(cell):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = tcPr.find(qn('w:tcBorders'))
    if tcBorders is None:
        tcBorders = OxmlElement('w:tcBorders')
        tcPr.append(tcBorders)
    for border_name in ['top', 'bottom', 'left', 'right']:
        border = tcBorders.find(qn(f'w:{border_name}'))
        if border is None:
            border = OxmlElement(f'w:{border_name}')
            tcBorders.append(border)
        border.set(qn('w:val'), 'none')

def limpar_espacamento_lista(paragraph):
    paragraph.paragraph_format.space_before = Pt(0)
    paragraph.paragraph_format.space_after = Pt(0)
    pPr = paragraph._element.get_or_add_pPr()
    spacing = OxmlElement('w:spacing')
    spacing.set(qn('w:line'), '240')
    spacing.set(qn('w:lineRule'), 'auto')
    if hasattr(pPr, 'spacing'):
        try: pPr.remove(pPr.spacing)
        except: pass
    pPr.append(spacing)