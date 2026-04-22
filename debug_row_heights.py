#!/usr/bin/env python
# -*- coding: utf-8 -*-

from docx import Document
from docx.oxml.ns import qn

def debug_row_heights():
    """Verifica as alturas das linhas diretamente no XML"""
    doc = Document('teste_metas_institucionais.docx')
    
    print("=" * 100)
    print("DEBUG: VERIFICAÇÃO DE ALTURAS NO XML")
    print("=" * 100)
    
    tabelas = doc.tables
    if len(tabelas) > 0:
        tabela = tabelas[0]
        print(f"\nPrimeira tabela (TJMG 5):\n")
        
        for row_idx, row in enumerate(tabela.rows):
            tr = row._tr
            trPr = tr.get_or_add_trPr()
            
            # Procura por trHeight
            trHeight = trPr.find(qn('w:trHeight'))
            
            print(f"Linha {row_idx + 1}:")
            print(f"  row.height (property): {row.height}")
            
            if trHeight is not None:
                height_val = trHeight.get(qn('w:val'))
                hRule = trHeight.get(qn('w:hRule'))
                print(f"  w:trHeight val: {height_val}")
                print(f"  w:trHeight hRule: {hRule}")
            else:
                print(f"  w:trHeight: NOT FOUND")
            
            print()

if __name__ == '__main__':
    debug_row_heights()
