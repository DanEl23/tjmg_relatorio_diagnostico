# 📋 FLUXO DE EXTRAÇÃO - extracao_cnj.py

## 🎯 OBJETIVO GERAL
Automatizar coleta de dados do painel Justiça em Números (https://justica-em-numeros.cnj.jus.br/painel-metas/) extraindo informações das 10 metas institucionais do TJMG.

---

## 🔄 FLUXO PRINCIPAL

```
1. Acessar URL do painel
   ↓
2. Entrar no iFrame PowerBI
   ↓
3. Para cada META (1-10):
   ├─ Clicar no elemento da meta (se aplicável)
   ├─ Aplicar filtros (Ramo de Justiça, Tribunal)
   ├─ Clicar em botões de ação (botões laranjas)
   └─ Extrair dados (KPIs e gráficos)
   ↓
4. Salvar em Excel (exports/resultados_cnj.xlsx)
```

---

## 📍 ETAPA 1: INICIALIZAÇÃO

### Passo 1.1 - Acessar Painel
```python
self.driver.get("https://justica-em-numeros.cnj.jus.br/painel-metas/")
time.sleep(10)
```
- **O QUE BUSCA:** Página principal do painel
- **TIMEOUT:** 10 segundos

### Passo 1.2 - Entrar no iFrame
```python
iframe = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe")))
self.driver.switch_to.frame(iframe)
```
- **O QUE BUSCA:** Tag `<iframe>` (PowerBI embedding)
- **IMPORTANTE:** Sem isso, os elementos PowerBI não são visíveis!

---

## 🎲 ETAPA 2: FILTROS GLOBAIS (Aplicados antes de cada META)

### Filtro 1 - Ramo da Justiça
```python
self.aplicar_filtro_powerbi("ramo_justica", "Justiça Estadual")
```
- **ONDE:** Dropdown PowerBI com `aria-label="ramo_justica"`
- **BUSCA:** Opção com `@title="Justiça Estadual"` ou `text()="Justiça Estadual"`
- **VARIANTE META 5:** Às vezes é "Tribunal" ao invés de "sigla_tribunal"

### Filtro 2 - Tribunal (TJMG)
```python
self.aplicar_filtro_powerbi("sigla_tribunal", "TJMG")
```
- **ONDE:** Dropdown PowerBI com `aria-label="sigla_tribunal"`
- **BUSCA:** Opção com `@title="TJMG"` ou `text()="TJMG"`
- **VARIANTE:** Algumas metas usam "Tribunal" ao invés de "sigla_tribunal"

---

## 🏗️ ESTRUTURA POR META

---

### ⭐ META 1
```
NOME: Meta 1 - Julgar mais processos que os distribuídos
SUBTÍTULO: (identificado automaticamente)
DESCRIÇÃO: (identificado automaticamente)

FLUXO:
1. Aplicar filtro "ramo_justica" → "Justiça Estadual"
2. Aplicar filtro "sigla_tribunal" → "TJMG"
3. EXTRAÇÃO:
   a) Gráfico de barras (extrair_dados_da_aba)
      - ONDE: Busca div[aria-label*="por Ramo"] ou [aria-label*="por Tribunal"]
      - ELEMENTOS:
        * Categorias: g.axis.y g.tick text
        * Valores: g.label-container tspan.label-tspan
      - RESULTADO: Lista de (Categoria, Valor)
   
   b) KPI "Julgar mais processos que os distribuídos" (extrair_kpi_meta_1_total)
      - ONDE: div[@title="Julgar mais processos que os distribuídos"]
      - BUSCA: text.value tspan
      - RESULTADO: Um valor único

ESTRUTURA XML BUSCADA:
├─ div[@title="Ou processos que foram distribuídos"]
│  └─ ...
│     └─ text[@class="value"]
│        └─ tspan → "99,23%" (VALOR CAPTURADO)

├─ div[aria-label*="por Ramo"]  (GRÁFICO)
│  └─ g.axis.y
│     ├─ g.tick text → "1º Grau"
│     ├─ g.tick text → "2º Grau"
│     └─ ...
│  └─ g.label-container
│     ├─ tspan.label-tspan → "99,23%"
│     ├─ tspan.label-tspan → "87,45%"
│     └─ ...
```

---

### ⭐ META 2
```
NOME: Meta 2 - Identificar e julgar ações de improbidade administrativa e crimes
SUBTÍTULO: "Identificar e julgar" (extraído de texto cinza)
DESCRIÇÃO: Valor de "Justiça Estadual"

FLUXO:
1. CLIQUE: Clicar em elemento com texto "Meta 2"
2. BOTÃO LARANJA: Clicar em botão laranja (índice 1)
   - ONDE: XPath contém fill="e1874d" (cor laranja)
   - ÍNDICE: O 2º botão laranja encontrado (índice 1, começando de 0)
3. Aplicar filtro "sigla_tribunal" → "TJMG"
4. EXTRAÇÃO:
   a) Cards (Cumprimento):
      - "1º Grau": div[@title="1º Grau"]/ancestor → h4 "Cumprimento" → p.bottom
      - "2º Grau": div[@title="2º Grau"]/ancestor → h4 "Cumprimento" → p.bottom
      - "Processos mais Antigos": div[@title="Processos mais Antigos"]/ancestor → ...
   
   b) Gráfico (Juizados e Turmas):
      - ONDE: g[@aria-label="Juizados e Turmas"]
      - BARRAS: rect (em ordem: Juizado Especial, Turma Recursal)
      - VALORES: aria-label de cada barra
      - CONVERSÃO: 0.9924 → 99,24%

ESTRUTURA XML BUSCADA:
├─ div[@title="1º Grau"]
│  └─ transform (ancestor)
│     ├─ h4 → "Cumprimento"
│     └─ p[@class="bottom"] → "89,45%" (VALOR CAPTURADO)

├─ g[@aria-label="Juizados e Turmas"]
│  ├─ rect[0] (aria-label="0.9923") → "Juizado Especial"
│  └─ rect[1] (aria-label="0.8765") → "Turma Recursal"
```

---

### ⭐ META 3
```
NOME: Meta 3
FLUXO:
1. CLIQUE: Clicar em "Meta 3"
2. Aplicar filtro "sigla_tribunal" → "TJMG"
3. EXTRAÇÃO:
   - ONDE: div[@title="Percentual de Cumprimento"]
   - BUSCA: text.value
   - RESULTADO: Um valor único (ex: "95,67%")
```

---

### ⭐ META 4
```
NOME: Meta 4 - Julgar ações de crimes contra a administração pública
DESCRIÇÃO: Dois tipos: "Crimes Contra Adm." + "Improbidade"

FLUXO:
1. CLIQUE: "Meta 4"
2. BOTÃO LARANJA: Índice 1
3. Aplicar filtro "sigla_tribunal" → "TJMG"
4. EXTRAÇÃO:
   a) Cards (Totais):
      - Card 1: div[@title="Meta 4"] → h4 "Cumprimento" → p.bottom
      - Card 2: div[@title="Meta 4 Improb. Administrativa"] → ...
   
   b) Gráfico (Detalhamento por Tribunal e Grau):
      - ONDE: div[@title="Cumprimento Meta 4 por Tribunal e Grau"]/ancestor::visualWrapper
      - SÉRIE 1: g[@aria-label="Meta 4"] (Verde Claro)
        * rect 0 → "2º Grau - Crimes Contra Adm."
        * rect 1 → "Juizado Especial - Crimes Contra Adm."
        * rect 2 → "Turma Recursal - Crimes Contra Adm."
        * rect 3 → "1º Grau - Crimes Contra Adm."
      
      - SÉRIE 2: g[@aria-label="Improb. Administrativa"] (Verde Escuro)
        * rect 0 → "2º Grau - Improbidade"
        * rect 1 → "Juizado Especial - Improbidade"
        * rect 2 → "1º Grau - Improbidade"

ESTRUTURA XML BUSCADA:
├─ div[@title="Meta 4"]
│  └─ transform (ancestor)
│     ├─ h4 → "Cumprimento"
│     └─ p.bottom → "78,90%" (VALOR 1)

├─ div[@title="Cumprimento Meta 4 por Tribunal e Grau"]
│  └─ ancestor::visualWrapper
│     ├─ g[@aria-label="Meta 4"]
│     │  ├─ rect data-automation-type="column-chart-rect" aria-label="0.7890"
│     │  ├─ rect data-automation-type="column-chart-rect" aria-label="0.6543"
│     │  └─ ...
│     └─ g[@aria-label="Improb. Administrativa"]
│        ├─ rect data-automation-type="column-chart-rect" aria-label="0.5432"
│        └─ ...
```

---

### ⭐ META 5
```
NOME: Meta 5 - Julgar ações cíveis em primeira instância
FLUXO:
1. CLIQUE: "Meta 5"
2. BOTÃO LARANJA: Índice 2 (mais um clique que outras metas!)
3. Aplicar filtro "Tribunal" → "TJMG" (NÃO é "sigla_tribunal"!)
4. EXTRAÇÃO:
   a) Card Total:
      - ONDE: div[@title="Cumprimento Meta 5"] ou "Percentual de Cumprimento"
      - BUSCA: text.value
   
   b) Gráfico (G1 e JE):
      - ONDE: g[@aria-label="Meta 5"]
      - BARRAS: rect[data-automation-type="column-chart-rect"]
      - FILTRA: Apenas barras com aria-label != "0"
      - MAPEAMENTO:
        * rect 0 → "1º Grau"
        * rect 1 → "Juizado Especial"

NOTA: Esta meta é diferentes - usa índice 2 e filtro "Tribunal"!
```

---

### ⭐ META 6
```
NOME: Meta 6 - Identificar e julgar ações de violência contra mulher
SUBTÍTULO: "Identificar e julgar"
DESCRIÇÃO: "Justiça Estadual"

FLUXO:
1. CLIQUE: "Meta 6"
2. BOTÃO LARANJA: Índice 1
3. Aplicar filtro:
   - TRY: "sigla_tribunal" → "TJMG"
   - EXCEPT: "Tribunal" → "TJMG"
4. EXTRAÇÃO:
   a) Card Total:
      - ONDE: Busca path[@data-sub-selection-display-name="Card_Background_Color"]
      - BUSCA em ancestor::visual-modern
      - VALUE: p.content ou text.value
   
   b) Gráfico:
      - ONDE: div[@title="Meta 6 por Tribunal e Grau"]
      - SÉRIE: g[@aria-label="Cumprimento Meta 6"]
      - BARRAS: rect[data-automation-type="column-chart-rect"]
      - MAPEAMENTO (Ordem visual):
        * rect 0 → "Turma Recursal"
        * rect 1 → "2º Grau"
        * rect 2 → "Juizado Especial"
        * rect 3 → "1º Grau"
```

---

### ⭐ META 7
```
NOME: Meta 7 - Identificar e julgar ações sobre direitos de povos indígenas e tribais
DESCRIÇÃO: Duas categorias

FLUXO:
1. CLIQUE: "Meta 7"
2. BOTÃO LARANJA: Índice 1
3. Aplicar filtro "sigla_tribunal" → "TJMG" (com fallback para "Tribunal")
4. EXTRAÇÃO:
   a) Card 1: div[@title="Meta 7 Indígenas"]
      - h4 "Cumprimento" → p.bottom
   
   b) Card 2: div[@title="Meta 7 Quilombola"]
      - h4 "Cumprimento" → p.bottom

RESULTADO: 2 valores ("Total Indígenas", "Total Quilombola")
```

---

### ⭐ META 8
```
NOME: Meta 8 - Identificar e julgar ações sobre violência doméstica e feminicídio
DESCRIÇÃO: Dois tipos: "Violência Doméstica" + "Feminicídio"

FLUXO:
1. CLIQUE: "Meta 8"
2. BOTÃO LARANJA: Índice 1
3. Aplicar filtro "sigla_tribunal" → "TJMG" (com fallback)
4. EXTRAÇÃO:
   a) Cards (Totais):
      - Card 1: div[@title="Violência Doméstica"] → h4 "Cumprimento" → p.bottom
      - Card 2: div[@title="Feminicídio"] → h4 "Cumprimento" → p.bottom
   
   b) Gráfico:
      - ONDE: div[@title="Meta 8 por Tribunal e Grau"]
      - SÉRIE 1: g[@aria-label="Cumprimento VD"]
        * rect 0 → "2º Grau - Violência Doméstica"
        * rect 1 → "1º Grau - Violência Doméstica"
        * rect 2 → "Juizado Especial - Violência Doméstica"
        * rect 3 → "Turma Recursal - Violência Doméstica"
      
      - SÉRIE 2: g[@aria-label="Cumprimento Feminicídio"]
        * rect 0 → "2º Grau - Feminicídio"
        * rect 1 → "1º Grau - Feminicídio"
        * rect 2 → "Juizado Especial - Feminicídio"
        (Nota: Pode ter menos barras que VD)
```

---

### ⭐ META 9
```
NOME: Meta 9
FLUXO:
1. CLIQUE: "Meta 9"
2. Aplicar filtro "sigla_tribunal" → "TJMG" (com fallback)
3. EXTRAÇÃO:
   - TRY: Busca por texto "Cumprimento"
   - EXCEPT: Busca por percentual solto (%)
   - RESULTADO: Um valor único

NOTA: Meta com menos estrutura/padrão definido
```

---

### ⭐ META 10
```
NOME: Meta 10
FLUXO:
1. CLIQUE: "Meta 10"
2. BOTÃO LARANJA: Índice 1
3. Aplicar filtro "sigla_tribunal" → "TJMG" (com fallback)
4. EXTRAÇÃO:
   a) Card 1: div[@title="1º Grau"] → h4 "Cumprimento" → p.bottom
   b) Card 2: div[@title="2º Grau"] → h4 "Cumprimento" → p.bottom

RESULTADO: 2 valores ("1º Grau", "2º Grau")
```

---

## 💾 ETAPA 3: SALVAR EM EXCEL

```python
df = pd.DataFrame(self.dados_extraidos)
arquivo = "exports/resultados_cnj.xlsx"
df.to_excel(arquivo, index=False)
```

### Estrutura do DataFrame:
```
┌──────────────────────┬─────────────────────┬──────────────┬──────────────┬──────────────────┐
│ Meta                 │ Descrição Completa  │ Categoria    │ Resultado    │ Data             │
├──────────────────────┼─────────────────────┼──────────────┼──────────────┼──────────────────┤
│ Meta 1               │ Descrição texto     │ Total        │ 99,23%       │ 2025-01-15 14:30 │
│ Meta 1               │ Descrição texto     │ 1º Grau      │ 89,45%       │ 2025-01-15 14:30 │
│ Meta 2               │ Texto - Subtítulo   │ Juizado Esp. │ 78,90%       │ 2025-01-15 14:32 │
│ ...                  │ ...                 │ ...          │ ...          │ ...              │
└──────────────────────┴─────────────────────┴──────────────┴──────────────┴──────────────────┘
```

---

## 🔍 SELETORES CRÍTICOS - RESUMO

| O QUE | SELETOR | TIPO |
|------|---------|------|
| iFrame | `iframe` (CSS) | iframe |
| Meta X Label | `//*[contains(text(), 'Meta X')]` | XPath |
| Filtro PowerBI | `//div[@class='slicer-dropdown-menu' and @aria-label='NOME']` | XPath |
| Valor do Card | `:text.value` ou `text.value tspan` | CSS/XPath |
| Barras Gráfico | `rect[data-automation-type='column-chart-rect']` | CSS |
| Série Gráfico | `g[@aria-label='NOME_SERIE']` | XPath |
| Botão Laranja | `//*[contains(@fill, 'e1874d')]` | XPath |

---

## ⚠️ PONTOS CRÍTICOS PARA DEBUG

1. **iFrame não encontrado** → Painel pode não usar PowerBI ou estrutura mudou
2. **Filtros não aplicam** → Nome do aria-label pode ser diferente (use F12!)
3. **Gráficos vazios** → rect pode ter a-label="0" (precisa filtrar)
4. **Valores formatados errado** → Decimais podem estar com `.` ao invés de `,`
5. **Timeouts** → Painel anterior pode ter carregamento mais lento
6. **Ordem das barras muda** → Difere de visualização para visualização

---

## 🛠️ COMO DEBUGAR

```python
# 1. Abra DevTools (F12) no navegador
# 2. Procure pelos elementos usando:
#    - Direita: Clique > Inspecionar
#    - Aba Console: Execute seletores JavaScript
#    - Aba Elementos: Veja a hierarquia XML/HTML

# 3. Teste seletores no console:
document.querySelectorAll("div[@title='Meta 1']")  # CSS
$x("//*[contains(text(), 'Meta 1')]")  # XPath

# 4. Inspecione aria-labels dos filtros:
document.querySelectorAll("[class*='slicer']")
```

---

## 📝 CHECKLIST PARA NOVO PAINEL

- [ ] URL diferente? Atualizar `self.driver.get()`
- [ ] iFrame ainda existe? Senão, remover `entrar_no_iframe()`
- [ ] Filtros têm os mesmos aria-labels? Verificar com F12
- [ ] Botões laranjas ainda existem? Ou foram removidos?
- [ ] Estrutura XML dos cards mudou?
- [ ] Gráficos usam SVG e rect? Ou outra tecnologia?
- [ ] Ordem das metas é a mesma?
- [ ] Nomes das séries dos gráficos mudaram?
