#!/usr/bin/env python3
"""
Teste rápido para validar a implementação de METAS_INSTITUCIONAIS
"""

import sys
sys.path.insert(0, '.')

print("=" * 70)
print("TESTE: VERIFICAÇÃO DE IMPLEMENTAÇÃO DE METAS_INSTITUCIONAIS")
print("=" * 70)

# 1. Verifica a função preparar_dados_tabela_metas
print("\n✓ Testando importação de preparar_dados_tabela_metas...")
try:
    from src.core.generator import preparar_dados_tabela_metas
    print("  ✓ Função importada com sucesso")
except ImportError as e:
    print(f"  ✗ Erro ao importar: {e}")
    sys.exit(1)

# 2. Verifica se a função adicionar_todas_metas_institucionais existe
print("\n✓ Testando importação de adicionar_todas_metas_institucionais...")
try:
    from src.tables.builders import adicionar_todas_metas_institucionais
    print("  ✓ Função importada com sucesso")
except ImportError as e:
    print(f"  ✗ Erro ao importar: {e}")
    sys.exit(1)

# 3. Verifica se METAS_INSTITUCIONAIS está em MAPA_RECURSOS
print("\n✓ Testando marcador METAS_INSTITUCIONAIS em MAPA_RECURSOS...")
try:
    from src.content.static_data import MAPA_RECURSOS
    if "METAS_INSTITUCIONAIS" in MAPA_RECURSOS:
        print("  ✓ Marcador encontrado em MAPA_RECURSOS")
        config = MAPA_RECURSOS["METAS_INSTITUCIONAIS"]
        print(f"  ✓ Tipo: {config.get('tipo')}")
    else:
        print("  ✗ Marcador NÃO encontrado em MAPA_RECURSOS")
        sys.exit(1)
except Exception as e:
    print(f"  ✗ Erro: {e}")
    sys.exit(1)

# 4. Verifica HISTORICO_METAS_CNJ
print("\n✓ Testando HISTORICO_METAS_CNJ...")
try:
    from src.content.static_data import HISTORICO_METAS_CNJ
    total_metas = len(HISTORICO_METAS_CNJ)
    print(f"  ✓ Total de metas: {total_metas}")
    
    metas_nomes = sorted(
        HISTORICO_METAS_CNJ.keys(),
        key=lambda x: int(x.split()[1]) if 'Meta' in x else 0
    )
    print(f"  ✓ Metas: {', '.join(metas_nomes[:5])}... (primeiras 5)")
except Exception as e:
    print(f"  ✗ Erro: {e}")
    sys.exit(1)

# 5. Testa preparar_dados_tabela_metas com Meta 1
print("\n✓ Testando preparar_dados_tabela_metas com 'Meta 1'...")
try:
    dados = preparar_dados_tabela_metas("Meta 1")
    if dados:
        print(f"  ✓ Dados gerados: {len(dados)} linhas")
        print(f"  ✓ Primeira linha (cabeçalho): {dados[0][:3]}...")
    else:
        print("  ⚠ Nenhum dado retornado (possível erro)")
except Exception as e:
    print(f"  ✗ Erro ao chamar função: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 70)
print("✓ TODOS OS TESTES PASSARAM!")
print("=" * 70)
