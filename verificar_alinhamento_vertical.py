#!/usr/bin/env python
# -*- coding: utf-8 -*-

from docx import Document
from docx.oxml.ns import qn

def verificar_alinhamento_vertical():
    """Verifica o alinhamento vertical das células do cabeçalho"""
    doc = Document('teste_metas_institucionais.docx')
    
    print("=" * 100)
    print("VERIFICAÇÃO DE ALINHAMENTO VERTICAL DO CABEÇALHO")
    print("=" * 100)
    
    tabelas = doc.tables
    if len(tabelas) > 0:
        tabela = tabelas[0]
        print(f"\nPrimeira tabela (TJMG 5):\n")
        
        # Verifica primeira linha (cabeçalho)
        print("Cabeçalho (Linha 1):")
        for col_idx, cell in enumerate(tabela.rows[0].cells):
            tcPr = cell._element.tcPr
            vAlign = tcPr.find(qn('w:vAlign')) if tcPr is not None else None
            
            if vAlign is not None:
                v_align_value = vAlign.get(qn('w:val'))
                print(f"  Coluna {col_idx + 1}: vAlign = '{v_align_value}' ✓")
            else:
                print(f"  Coluna {col_idx + 1}: vAlign não encontrado")
        
        # Verifica segunda linha para comparação
        print("\nSegunda linha (Dados - Meta):")
        for col_idx, cell in enumerate(tabela.rows[1].cells):
            tcPr = cell._element.tcPr
            vAlign = tcPr.find(qn('w:vAlign')) if tcPr is not None else None
            
            if vAlign is not None:
                v_align_value = vAlign.get(qn('w:val'))
                print(f"  Coluna {col_idx + 1}: vAlign = '{v_align_value}'")
            else:
                print(f"  Coluna {col_idx + 1}: vAlign não definido (padrão)")
    
    print("\n" + "=" * 100)
    print("✓ VERIFICAÇÃO CONCLUÍDA")
    print("=" * 100)

if __name__ == '__main__':
    verificar_alinhamento_vertical()
