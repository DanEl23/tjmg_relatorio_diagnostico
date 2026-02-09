"""
Testes para o módulo de extração CNJ.
Valida funcionalidades de detecção de cores cinza e busca de texto.
"""

import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.extractors.extracao_cnj import GrayColorDetector, TextSearcher


def test_gray_color_detector():
    """Testa o detector de cores cinza."""
    print("="*60)
    print("Teste: GrayColorDetector")
    print("="*60)
    
    detector = GrayColorDetector()
    
    # Teste 1: Cores cinza válidas
    test_cases_gray = [
        (0x000000, "Preto (cinza escuro)"),
        (0x404040, "Cinza escuro"),
        (0x808080, "Cinza médio"),
        (0xBFBFBF, "Cinza claro"),
        (0xDDDDDD, "Cinza muito claro"),
        (0x333333, "Cinza escuro #333"),
        (0x999999, "Cinza médio #999"),
    ]
    
    print("\n✅ Testando cores CINZA (devem retornar True):")
    for color, description in test_cases_gray:
        result = detector.is_gray(color)
        status = "✓" if result else "✗"
        print(f"  {status} #{color:06X} - {description}: {result}")
        assert result == True, f"Esperado True para {description}"
    
    # Teste 2: Cores não-cinza
    test_cases_not_gray = [
        (0xFF0000, "Vermelho puro"),
        (0x00FF00, "Verde puro"),
        (0x0000FF, "Azul puro"),
        (0xFF8800, "Laranja"),
        (37509, "Verde CNJ"),  # Cor específica do CNJ
    ]
    
    print("\n❌ Testando cores NÃO-CINZA (devem retornar False):")
    for color, description in test_cases_not_gray:
        result = detector.is_gray(color)
        status = "✓" if not result else "✗"
        print(f"  {status} #{color:06X} - {description}: {result}")
        assert result == False, f"Esperado False para {description}"
    
    # Teste 3: Adicionar intervalo customizado
    print("\n🔧 Testando adição de intervalo customizado:")
    # Testa uma cor que ainda não está nos intervalos padrão
    custom_color = 0xF5F5F5
    initial_result = detector.is_gray(custom_color)
    print(f"  ✓ Cor #{custom_color:06X} inicialmente detectada como cinza: {initial_result}")
    assert initial_result == False, f"Cor {custom_color:06X} deveria ser False antes de adicionar intervalo"
    
    # Adiciona um intervalo específico para cores muito claras
    detector.add_gray_range(0xF0F0F0, 0xFFFFFF)
    new_result = detector.is_gray(custom_color)
    print(f"  ✓ Intervalo customizado (0xF0F0F0-0xFFFFFF) adicionado")
    print(f"  ✓ Cor #{custom_color:06X} agora detectada: {new_result}")
    assert new_result == True, f"Cor {custom_color:06X} deveria ser detectada após adicionar intervalo"
    
    # Teste 4: Validação de cores não-cinza
    print("\n⚠️  Testando validação de cores não-cinza:")
    try:
        detector.add_gray_range(0xFF0000, 0xFF00FF)  # Vermelho a roxo - não é cinza
        assert False, "Deveria ter lançado ValueError"
    except ValueError as e:
        print(f"  ✓ ValueError corretamente lançado: {str(e)[:60]}...")
    
    print("\n✅ Todos os testes do GrayColorDetector passaram!")


def test_text_searcher():
    """Testa o buscador de texto."""
    print("\n" + "="*60)
    print("Teste: TextSearcher")
    print("="*60)
    
    searcher = TextSearcher()
    
    # Teste 1: Padrões de gráficos
    test_cases_graphs = [
        ("Figura 01 - Descrição do gráfico", True),
        ("Gráfico 123 - Outro gráfico", True),
        ("Quadro 5 - Tabela de dados", True),
        ("Figura 1", True),
        ("Gráfico 999", True),
        ("  Figura 01 - Com espaços  ", True),
        ("FIGURA 10 - MAIÚSCULAS", True),
        ("figura 2 - minúsculas", True),
    ]
    
    print("\n✅ Testando CORRESPONDÊNCIAS válidas:")
    for text, expected in test_cases_graphs:
        matches = searcher.search_all_patterns(text)
        result = len(matches) > 0
        status = "✓" if result == expected else "✗"
        print(f"  {status} '{text}': {result} (esperado: {expected})")
        assert result == expected, f"Falha para texto: {text}"
    
    # Teste 2: Textos que NÃO devem corresponder
    test_cases_no_match = [
        ("Apenas texto normal", False),
        ("Figura sem número", False),
        ("Gráfico X", False),
        ("123 Figura invertido", False),
        ("Um parágrafo qualquer", False),
    ]
    
    print("\n❌ Testando textos SEM correspondência:")
    for text, expected in test_cases_no_match:
        matches = searcher.search_all_patterns(text)
        result = len(matches) > 0
        status = "✓" if result == expected else "✗"
        print(f"  {status} '{text}': {result} (esperado: {expected})")
        assert result == expected, f"Falha para texto: {text}"
    
    # Teste 3: Adicionar padrão customizado
    print("\n🔧 Testando adição de padrão customizado:")
    custom_pattern = r"Anexo\s+[A-Z]"
    searcher.add_pattern(custom_pattern)
    test_text = "Anexo A - Documento adicional"
    matches = searcher.search_all_patterns(test_text)
    print(f"  ✓ Padrão customizado '{custom_pattern}' adicionado")
    print(f"  ✓ Texto '{test_text}' encontrado: {len(matches) > 0}")
    assert len(matches) > 0, "Padrão customizado não funcionou"
    
    # Teste 4: Busca por padrão específico
    print("\n🔍 Testando busca por índice de padrão:")
    text = "Figura 25 - Teste"
    match_0 = searcher.search_text(text, pattern_index=0)
    match_1 = searcher.search_text(text, pattern_index=1)
    print(f"  ✓ Padrão 0 (Figuras): {match_0 is not None}")
    print(f"  ✓ Padrão 1 (Tabelas): {match_1 is not None}")
    assert match_0 is not None, "Deveria encontrar com padrão 0"
    
    print("\n✅ Todos os testes do TextSearcher passaram!")


def test_integration():
    """Testa integração entre os componentes."""
    print("\n" + "="*60)
    print("Teste: Integração")
    print("="*60)
    
    detector = GrayColorDetector()
    searcher = TextSearcher()
    
    # Simula processamento de uma legenda
    simulated_legend = {
        "text": "Figura 10 - Taxa de congestionamento",
        "color": 0x808080,  # Cinza médio
    }
    
    print(f"\n📄 Simulando extração de legenda:")
    print(f"   Texto: '{simulated_legend['text']}'")
    print(f"   Cor: #{simulated_legend['color']:06X}")
    
    # Verifica se o texto corresponde a um padrão
    matches = searcher.search_all_patterns(simulated_legend["text"])
    is_legend = len(matches) > 0
    print(f"   ✓ É uma legenda válida: {is_legend}")
    assert is_legend, "Deveria detectar como legenda"
    
    # Verifica se a cor é cinza
    is_gray = detector.is_gray(simulated_legend["color"])
    print(f"   ✓ Cor é cinza: {is_gray}")
    assert is_gray, "Deveria detectar cor como cinza"
    
    # Verifica se passaria no filtro
    would_extract = is_legend and is_gray
    print(f"   ✓ Seria extraída: {would_extract}")
    assert would_extract, "Deveria ser extraída"
    
    print("\n✅ Teste de integração passou!")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("TESTES DO MÓDULO DE EXTRAÇÃO CNJ")
    print("Suporte a Múltiplas Cores de Cinza e Busca por Texto")
    print("="*60)
    
    try:
        test_gray_color_detector()
        test_text_searcher()
        test_integration()
        
        print("\n" + "="*60)
        print("✅ TODOS OS TESTES PASSARAM COM SUCESSO!")
        print("="*60)
        
    except AssertionError as e:
        print(f"\n❌ TESTE FALHOU: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERRO INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
