# Sistema de Cores de Cinza - Documentação

## CORRIGIDO: Suporte a Múltiplas Cores de Cinza e Busca por Texto

Esta documentação descreve o sistema centralizado de gerenciamento de cores de cinza implementado no projeto.

## Visão Geral

O sistema fornece:
1. **Cores de cinza centralizadas** - Definidas em um único local (`src/config.py`)
2. **Busca de texto aprimorada** - Suporte a filtros de cor na extração de PDF
3. **Consistência visual** - Todas as tabelas usam o mesmo padrão de cores

## Cores Disponíveis

### Hierarquia de Cinzas (do mais escuro ao mais claro)

```python
from src.config import Colors

Colors.GRAY_DARK        # '7F7F7F' - Cinza escuro (cabeçalhos principais)
Colors.GRAY_MEDIUM      # 'BFBFBF' - Cinza médio (linhas de totais)
Colors.GRAY_LIGHT       # 'D9D9D9' - Cinza claro (sub-cabeçalhos)
Colors.GRAY_VERY_LIGHT  # 'EEEEEE' - Cinza muito claro (zebrado)
```

### Aliases para Compatibilidade

```python
Colors.HEADER_GRAY       # Alias para GRAY_DARK
Colors.HEADER_LIGHT_GRAY # Alias para GRAY_LIGHT
Colors.ZEBRA_STRIPE      # Alias para GRAY_VERY_LIGHT
Colors.TOTAL_ROW         # Alias para GRAY_MEDIUM
```

## Uso em Tabelas

### Antes (Hardcoded)

```python
def adicionar_tabela_exemplo(document, dados):
    COR_CABECALHO = '7F7F7F'  # Hardcoded
    COR_ZEBRADO = 'EEEEEE'    # Hardcoded
    
    shading.set(qn('w:fill'), '7F7F7F')
```

### Depois (Centralizado)

```python
from src.config import Colors

def adicionar_tabela_exemplo(document, dados):
    COR_CABECALHO = Colors.GRAY_DARK
    COR_ZEBRADO = Colors.GRAY_VERY_LIGHT
    
    shading.set(qn('w:fill'), Colors.GRAY_DARK)
```

## Métodos Auxiliares

### Obter Todas as Cores

```python
from src.config import Colors

todas_as_cores = Colors.get_all_grays()
# Retorna: {
#     'dark': '7F7F7F',
#     'medium': 'BFBFBF',
#     'light': 'D9D9D9',
#     'very_light': 'EEEEEE'
# }
```

### Obter Cor por Intensidade

```python
from src.config import Colors

cor = Colors.get_gray_by_intensity('dark')      # Retorna '7F7F7F'
cor = Colors.get_gray_by_intensity('light')     # Retorna 'D9D9D9'
cor = Colors.get_gray_by_intensity('invalid')   # Retorna 'D9D9D9' (default)
```

## Busca de Texto em PDFs

### Busca Simples (Sem Filtro de Cor)

```python
from src.extractors.pdf_extractor import buscar_texto_por_cor

# Busca todas as ocorrências do padrão, independente da cor
resultados = buscar_texto_por_cor(
    page=pagina_pdf,
    texto_pattern=r"Gráfico\s+\d+",
    cor_alvo=None  # Sem filtro de cor
)

for resultado in resultados:
    print(f"Texto: {resultado['texto']}")
    print(f"Posição: {resultado['bbox']}")
    print(f"Cor: {resultado['cor']}")
```

### Busca com Filtro de Cor Única

```python
from src.extractors.pdf_extractor import buscar_texto_por_cor
from src.config import Colors

# Busca apenas textos com cor específica (ex: legendas verdes)
resultados = buscar_texto_por_cor(
    page=pagina_pdf,
    texto_pattern=r"Figura\s+\d+",
    cor_alvo=Colors.PDF_LEGEND_GREEN,
    tolerancia=5000  # Aceita cores próximas
)
```

### Busca com Múltiplas Cores

```python
from src.extractors.pdf_extractor import buscar_texto_multiplas_cores

# Busca textos que podem estar em diferentes tons de cinza
cores_possiveis = [
    37509,   # Verde das legendas
    8355711, # Cinza escuro
    13816530 # Cinza claro
]

resultados = buscar_texto_multiplas_cores(
    page=pagina_pdf,
    texto_pattern=r"(Figura|Gráfico)\s+\d+",
    cores_alvo=cores_possiveis,
    tolerancia=5000
)

# Remove automaticamente duplicatas baseado na posição
```

## Extração de Imagens com Filtro de Cor

### Modo Padrão (Sem Filtro)

```python
from src.extractors.pdf_extractor import extrair_imagens

# Extrai todas as imagens, sem filtrar por cor
mapeamento = extrair_imagens()
```

### Com Filtro de Cor

```python
from src.extractors.pdf_extractor import extrair_imagens
from src.config import Colors

# Extrai apenas imagens com legendas em cores específicas
mapeamento = extrair_imagens(
    usar_filtro_cor=True,
    cores_legendas=[Colors.PDF_LEGEND_GREEN, 8355711]
)

# O mapeamento incluirá informações de cor
for nome, info in mapeamento.items():
    print(f"{nome}: cor={info['cor_texto']}")
```

## Benefícios

### Antes
- ❌ 38 valores hardcoded espalhados pelo código
- ❌ Difícil alterar esquema de cores
- ❌ Inconsistências entre tabelas
- ❌ Extração de PDF limitada a padrões de texto

### Depois
- ✅ Sistema centralizado em `src/config.py`
- ✅ Fácil manutenção e customização
- ✅ Consistência garantida
- ✅ Busca avançada com filtros de cor
- ✅ Suporte a múltiplos tons de cinza
- ✅ Métodos auxiliares para facilitar uso

## Arquivos Modificados

1. **src/config.py**
   - Adicionadas constantes GRAY_DARK, GRAY_MEDIUM, GRAY_LIGHT, GRAY_VERY_LIGHT
   - Métodos get_all_grays() e get_gray_by_intensity()
   
2. **src/tables/builders.py**
   - Importa Colors de src.config
   - 38 substituições de valores hardcoded por constantes
   
3. **src/extractors/pdf_extractor.py**
   - Novas funções buscar_texto_por_cor() e buscar_texto_multiplas_cores()
   - Função extrair_imagens() com suporte a filtro de cor

## Compatibilidade

O sistema mantém **100% de compatibilidade** com código existente através dos aliases:
- `Colors.HEADER_GRAY` → `Colors.GRAY_DARK`
- `Colors.HEADER_LIGHT_GRAY` → `Colors.GRAY_LIGHT`
- `Colors.ZEBRA_STRIPE` → `Colors.GRAY_VERY_LIGHT`
- `Colors.TOTAL_ROW` → `Colors.GRAY_MEDIUM`

## Testes

Execute o teste de tabelas para verificar o funcionamento:

```bash
python teste_tabelas.py
```

Resultado esperado:
```
--- 🚀 Teste Específico: Tabela de 4 Colunas ---
✅ Arquivo gerado com sucesso: teste_4_colunas.docx
```
