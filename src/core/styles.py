# ARQUIVO: src/core/styles.py
from docx.shared import Pt, RGBColor, Cm

# Definição da Cor Institucional (Vinho)
COR_VINHO = RGBColor(162, 22, 18)
COR_PRETO = RGBColor(0, 0, 0)

def configurar_estilos_doc(document):
    """
    Configura os estilos Heading 1, 2 e 3 do documento para o padrão TJMG.
    """
    styles = document.styles

    # --- Heading 1 (Ex: 3. TÍTULO) ---
    h1 = styles['Heading 1']
    h1.font.name = 'Calibri'
    h1.font.size = Pt(16)
    h1.font.bold = True
    h1.font.color.rgb = COR_VINHO
    h1.paragraph_format.space_before = Pt(18)
    h1.paragraph_format.space_after = Pt(12)
    h1.paragraph_format.left_indent = Cm(0) # Sem recuo

    # --- Heading 2 (Ex: 3.1 Subtítulo) ---
    h2 = styles['Heading 2']
    h2.font.name = 'Calibri'
    h2.font.size = Pt(14)
    h2.font.bold = True
    h2.font.color.rgb = COR_VINHO
    h2.paragraph_format.space_before = Pt(12)
    h2.paragraph_format.space_after = Pt(6)
    h2.paragraph_format.left_indent = Cm(0.5) # Recuo de 0.5cm

    # --- Heading 3 (Ex: 3.1.1 Sub-subtítulo) ---
    h3 = styles['Heading 3']
    h3.font.name = 'Calibri'
    h3.font.size = Pt(12)
    h3.font.bold = True
    h3.font.color.rgb = COR_VINHO
    h3.paragraph_format.space_before = Pt(12)
    h3.paragraph_format.space_after = Pt(6)
    h3.paragraph_format.left_indent = Cm(1.0) # Recuo de 1.0cm

def formatar_titulo_manualmente(run):
    """ Caso o estilo falhe, esta função força a cor no texto """
    run.font.color.rgb = COR_VINHO