# Módulo de Extração CNJ

## Descrição

Este módulo (`extracao_cnj.py`) fornece funcionalidades avançadas para extrair imagens e dados do PDF "Justiça em Números" do CNJ (Conselho Nacional de Justiça).

## Características Principais

### ✅ Suporte a Múltiplas Cores de Cinza

O módulo implementa um detector inteligente de cores cinza (`GrayColorDetector`) que:

- **Detecta múltiplos tons de cinza** - Suporta 4 intervalos padrão:
  - Cinza escuro/preto (0x000000 - 0x404040)
  - Cinza médio-escuro (0x404040 - 0x808080)
  - Cinza médio (0x808080 - 0xBFBFBF)
  - Cinza claro (0xBFBFBF - 0xE0E0E0)

- **Validação RGB inteligente** - Verifica se R ≈ G ≈ B com tolerância de 30 pontos

- **Extensível** - Permite adicionar intervalos customizados via `add_gray_range()`

### 🔍 Busca por Texto Avançada

O módulo implementa um buscador de texto (`TextSearcher`) que:

- **Detecta legendas** - Identifica padrões como:
  - "Figura 1", "Figura 01 - Descrição"
  - "Gráfico 123 - Título"
  - "Quadro 5 - Dados"
  - "Tabela 10"

- **Case-insensitive** - Funciona com MAIÚSCULAS, minúsculas ou MiStUrAdO

- **Múltiplos padrões** - Suporta vários padrões regex simultaneamente

- **Extensível** - Permite adicionar padrões customizados via `add_pattern()`

## Como Usar

### Uso Básico

```python
from src.extractors.extracao_cnj import extrair_imagens_cnj

# Extrai imagens com todas as funcionalidades habilitadas
mapeamento = extrair_imagens_cnj(
    color_filter=True,           # Filtra por cores (verde CNJ + cinza)
    use_gray_detector=True,      # Usa detector de múltiplos tons de cinza
    custom_patterns=None         # Usa padrões padrão
)

print(f"{len(mapeamento)} imagens extraídas!")
```

### Uso Avançado - GrayColorDetector

```python
from src.extractors.extracao_cnj import GrayColorDetector

detector = GrayColorDetector()

# Testar se uma cor é cinza
cor_hexadecimal = 0x808080  # Cinza médio
if detector.is_gray(cor_hexadecimal):
    print("É cinza!")

# Adicionar intervalo customizado
detector.add_gray_range(0xF0F0F0, 0xFFFFFF)  # Cinza muito claro
```

### Uso Avançado - TextSearcher

```python
from src.extractors.extracao_cnj import TextSearcher

searcher = TextSearcher()

# Buscar por padrões
texto = "Figura 10 - Taxa de congestionamento"
matches = searcher.search_all_patterns(texto)

if matches:
    print(f"Encontrado {len(matches)} correspondências!")

# Adicionar padrão customizado
searcher.add_pattern(r"Anexo\s+[A-Z]")
```

## Saída

O módulo gera:

1. **Imagens PNG** - Salvas em `data/processed/extracted_images/`
2. **JSON de Mapeamento** - Arquivo `mapeamento_graficos_completo.json` contendo:

```json
{
    "Figura 1": {
        "pagina": 42,
        "caminho_completo": "/path/to/Figura 1.png",
        "status": "encontrado",
        "cor": "#808080",
        "tipo_cor": "cinza"
    }
}
```

3. **Estatísticas** - Relatório no console com:
   - Total de páginas processadas
   - Legendas encontradas (verde, cinza, outras)
   - Imagens extraídas

## Testes

Execute os testes para validar a funcionalidade:

```bash
python tests/test_extracao_cnj.py
```

Os testes cobrem:
- ✅ Detecção de cores cinza (7 casos de teste)
- ✅ Rejeição de cores não-cinza (5 casos de teste)
- ✅ Adição de intervalos customizados
- ✅ Busca por padrões de texto (8 casos válidos, 5 inválidos)
- ✅ Adição de padrões customizados
- ✅ Integração entre componentes

## Arquitetura

```
extracao_cnj.py
├── GrayColorDetector      # Detecta múltiplos tons de cinza
│   ├── is_gray()          # Verifica se cor é cinza
│   └── add_gray_range()   # Adiciona intervalo customizado
│
├── TextSearcher           # Busca padrões de texto
│   ├── search_text()      # Busca por padrão específico
│   ├── search_all_patterns() # Busca todos os padrões
│   └── add_pattern()      # Adiciona padrão customizado
│
└── extrair_imagens_cnj()  # Função principal de extração
```

## Dependências

- `PyMuPDF` (fitz) - Processamento de PDF
- `pathlib` - Manipulação de caminhos
- `re` - Expressões regulares
- `json` - Serialização de dados

## Notas de Implementação

### Por que Múltiplas Cores de Cinza?

O PDF "Justiça em Números" usa diferentes tons de cinza para legendas, dependendo:
- Da versão do PDF
- Do tipo de gráfico
- Da renderização do documento

Um detector com um único tom de cinza perderia muitas legendas válidas.

### Por que Busca por Texto?

A busca por texto permite:
- Identificar legendas mesmo quando o formato muda
- Suportar novos padrões sem modificar o código principal
- Validar se o texto extraído é realmente uma legenda

## TODO / Melhorias Futuras

- [ ] Adicionar suporte a cores customizadas além de verde e cinza
- [ ] Implementar cache de resultados para PDFs já processados
- [ ] Adicionar opção de extrair apenas páginas específicas
- [ ] Suporte a processamento paralelo para PDFs grandes
- [ ] Interface CLI para uso independente

## Autor

Implementado como parte do projeto TJMG Relatório Diagnóstico.

## Licença

[Adicionar informação de licença]
