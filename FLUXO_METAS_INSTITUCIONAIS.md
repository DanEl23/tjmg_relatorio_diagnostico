#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
DOCUMENTAÇÃO: FLUXO DE PROCESSAMENTO DAS METAS INSTITUCIONAIS

Este arquivo documenta o fluxo completo de como as tabelas das metas institucionais
são inseridas no documento final através do sistema de marcadores.
"""

print("""
╔════════════════════════════════════════════════════════════════════════════════╗
║         FLUXO DE PROCESSAMENTO DAS METAS INSTITUCIONAIS NO RELATÓRIO          ║
╚════════════════════════════════════════════════════════════════════════════════╝

PASSO 1: ARQUIVO FONTE COM MARCADOR
═══════════════════════════════════════════════════════════════════════════════

  📄 Conteudo_Fonte.docx
  ├── ... (parágrafos anteriores)
  ├── [FINALIZAR_LISTA_MARCADORES]
  ├── [QUEBRA_PAGINA]
  ├── 11. METAS INSTITUCIONAIS DO TJMG
  ├── Apresentação das 55 metas institucionais do TJMG para o ano de 2025...
  │
  ├── **METAS_INSTITUCIONAIS**  ←─── MARCADOR QUE SERÁ PROCESSADO
  │
  ├── 12. CONCLUSÃO
  └── ... (parágrafos posteriores)


PASSO 2: MAPEAMENTO DE RECURSOS EM static_data.py
═══════════════════════════════════════════════════════════════════════════════

  MAPA_RECURSOS = {
      ...
      "METAS_INSTITUCIONAIS": {
          "tipo": "METAS_INSTITUCIONAIS",
          "fonte_custom": "Fonte: Painel Metas Nacionais CNJ..."
      }
      ...
  }

  ✓ A chave "METAS_INSTITUCIONAIS" faz correspondência com o marcador no Word
  ✓ O tipo sinaliza qual função builder deve ser chamada


PASSO 3: LEITURA E PROCESSAMENTO NO GERADOR
═══════════════════════════════════════════════════════════════════════════════

  src/core/generator.py - Função: gerar_relatorio_completo()
  
  Linha 685-714: Para cada parágrafo em Conteudo_Fonte.docx
  ───────────────────────────────────────────────────────────
  for para in doc_fonte.paragraphs:
      texto = para.text.strip()
      
      # Verifica se o texto está no MAPA_RECURSOS
      if texto in mapa:
          processar_recurso(doc_final, texto, mapa[texto], loader_jn=loader_jn)
          continue


  Quando encontra "METAS_INSTITUCIONAIS":
  ─────────────────────────────────────────
  ✓ texto = "METAS_INSTITUCIONAIS"
  ✓ texto in mapa → TRUE
  ✓ Chama: processar_recurso(doc_final, "METAS_INSTITUCIONAIS", 
                               {"tipo": "METAS_INSTITUCIONAIS", ...}, 
                               loader_jn)


PASSO 4: PROCESSAMENTO DO RECURSO
═══════════════════════════════════════════════════════════════════════════════

  src/core/generator.py - Função: processar_recurso()
  
  Linha 601-602:
  ─────────────
  elif tipo == "METAS_INSTITUCIONAIS":
      builders.adicionar_todas_metas_institucionais(doc, loader_jn=loader_jn)


PASSO 5: LEITURA DO EXCEL E CONSTRUÇÃO DAS TABELAS
═══════════════════════════════════════════════════════════════════════════════

  src/tables/builders.py - Função: adicionar_todas_metas_institucionais()
  
  Para cada uma das 55 metas em exports/metas_institucionais_2025.xlsx:
  ──────────────────────────────────────────────────────────────────────
  
  1. Lê a meta do Excel (coluna Meta)
  2. Extrai dados dos anos 2022-2025
  3. Cria tabela formatada:
     - Título (ex: "TJMG 5")
     - Descrição (ex: "Realizar, em 2025, 70% dos julgamentos...")
     - Tabela com 3 linhas x 5 colunas:
       • Linha 1: Cabeçalho (2022, 2023, 2024, 2025, Meta)
       • Linha 2: Valores históricos (dados)
       • Linha 3: Legenda/Fonte
  4. Aplica formatação (cores RGB, alturas, fontes, alinhamentos)
  5. Adiciona propriedades de quebra de página (keep_with_next, cantSplit)


PASSO 6: INSERÇÃO NO DOCUMENTO FINAL
═══════════════════════════════════════════════════════════════════════════════

  📄 Relatorio_Com_Metas_Final_v2.docx
  ├── ... (Capa, Sumário, seções anteriores)
  │
  ├── 11. METAS INSTITUCIONAIS DO TJMG
  │   (Gerado a partir do Conteudo_Fonte.docx - parágrafo anterior ao marcador)
  │
  ├── [AQUI COMEÇAM AS 55 METAS GERADAS]
  │
  ├── TJMG 5
  │   └── [Tabela formatada: histórico + dados + legenda]
  │
  ├── TJMG 6
  │   └── [Tabela formatada: histórico + dados + legenda]
  │
  ├── ... (mais 53 metas)
  │
  ├── TJMG 156
  │   └── [Tabela formatada: histórico + dados + legenda]
  │
  ├── 12. CONCLUSÃO
  └── ... (parágrafos finais)


RESUMO DO SISTEMA
═══════════════════════════════════════════════════════════════════════════════

┌─────────────────────────┐
│  Conteudo_Fonte.docx    │  Marcador: "METAS_INSTITUCIONAIS"
└────────────┬────────────┘
             │ (texto in mapa?)
             ▼
┌─────────────────────────┐
│   processar_recurso()   │  Procura em MAPA_RECURSOS
└────────────┬────────────┘
             │ (tipo == "METAS_INSTITUCIONAIS")
             ▼
┌─────────────────────────┐
│ adicionar_todas_metas   │  Lê Excel + cria tabelas
│ _institucionais()       │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│ Relatório Final com 55 Metas Inseridas  │
└─────────────────────────────────────────┘


ARQUIVOS ENVOLVIDOS
═══════════════════════════════════════════════════════════════════════════════

1. data/raw/Conteudo_Fonte.docx
   ├─ Contém o marcador "METAS_INSTITUCIONAIS" em um parágrafo
   └─ Processado linha por linha

2. src/content/static_data.py
   ├─ Define MAPA_RECURSOS com chave "METAS_INSTITUCIONAIS"
   └─ Especifica tipo e configurações

3. src/core/generator.py
   ├─ Função: gerar_relatorio_completo() - Lê Conteudo_Fonte
   ├─ Função: processar_recurso() - Identifica tipo e chama builder
   └─ Orquestra o fluxo completo

4. src/tables/builders.py
   ├─ Função: adicionar_todas_metas_institucionais()
   ├─ Lê: exports/metas_institucionais_2025.xlsx
   └─ Gera: Tabelas formatadas com 55 metas

5. exports/metas_institucionais_2025.xlsx
   ├─ Sheet "Valores Apurados": 55 metas com dados 2022-2025
   └─ Sheet "Textos Metas": Descrições e metas


RESULTADO FINAL
═══════════════════════════════════════════════════════════════════════════════

✓ 55 metas institucionais completamente formatadas
✓ Cada meta com tabela individual (3 linhas x 5 colunas)
✓ Formatação consistente com cores, fontes e tamanhos especificados
✓ Totais de 1.290 parágrafos e 141 tabelas no documento final
✓ Sem quebras indesejadas entre título/tabela/legenda
""")
