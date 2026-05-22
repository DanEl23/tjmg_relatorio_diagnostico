# 🔄 DIFERENÇAS - PAINEL ANTIGO vs. NOVO

## 1. KPI (Card com Métrica)

### ❌ PAINEL ANTIGO (Esperado)
```xpath
//div[@title='Julgar mais processos que os distribuídos']
  └─ text.value
     └─ tspan → "106,70%"
```

### ✅ PAINEL NOVO (HTML Real)
```xpath
//transform[@aria-label='Julgar mais processos que os distribuídos']
  └─ text.value tspan → "106,70%"
```

**Mudança:** `div[@title]` → `transform[@aria-label]`

---

## 2. GRÁFICO - Valores nas Barras

### ❌ PAINEL ANTIGO
As barras usavam aria-label com decimais, precisava converter:
```xpath
rect[@aria-label="0.9923"]  # Decimal
// Converter: 0.9923 * 100 = 99,23%
```

### ✅ PAINEL NOVO
As barras têm ar-label decimal, MAS os rótulos já estão formatados:
```xpath
rect[@aria-label="1.234657405025298"]  # Decimal (ignorar!)
tspan[@class="label-tspan"]            # USAR ISSO!
  └─ "123,47%" (já formatado!)
```

**Mudança:** Usar `tspan.label-tspan` ao invés de converter aria-label das barras

---

## 3. EIXO Y (Categorias)

### ❌ PAINEL ANTIGO
Showava instâncias (Graus):
```
- 1º Grau
- 2º Grau
- Juizado Especial
- Turma Recursal
```

### ✅ PAINEL NOVO
Mostra RAMOS de justiça:
```
- Justiça Federal
- Justiça Militar Estadual
- Justiça Eleitoral
- Justiça Estadual        ← TJMG está aqui
- Justiça do Trabalho
- Justiça Militar da União
- Tribunais Superiores
```

**Impacto:** Precisamos de um novo mapeamento de categorias!

---

## 📋 CHECKLIST DE CORREÇÕES

- [x] Usar `transform[@aria-label]` para KPIs
- [x] Extrair valores de `tspan[@class='label-tspan']` (já formatados)
- [x] Mapear RAMOS ao invés de GRAUS
- [x] Buscar gráficos por `h3` ao invés de `div[@title]`
- [ ] Validar se filtros ainda funcionam (sigla_tribunal, ramo_justica)

---

## 🧪 PRÓXIMO TESTE

Execute com a URL do painel anterior:
```powershell
python src/extractors/extracao_novo_painel.py
```

**Esperado:**
```
=== 🏁 INICIANDO META 1 ===
--- Extração Gráfico (Meta 1) ---
   > Encontrados 7 rótulos formatados
   💎 Categoria 1: 123,47%
   💎 Categoria 2: 117,14%
   ...
--- Extração KPI Simples (Meta 1) ---
   💎 Valor encontrado (Meta 1): 106,70%
✅ Arquivo salvo: exports/resultados_novo_painel.xlsx
```

Se funcionar, vamos adaptar as outras metas! ✨
