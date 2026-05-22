"""
🔍 SCRIPT DE DIAGNÓSTICO - Explorar estrutura do painel anterior
Objetivo: Identificar quais elementos realmente existem
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

class DiagnosticoPainel:
    def __init__(self):
        print("🔧 Inicializando diagnóstico...")
        opcoes = webdriver.ChromeOptions()
        opcoes.add_argument('--start-maximized')
        opcoes.add_argument('--disable-notifications')
        
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=opcoes
        )
        self.wait = WebDriverWait(self.driver, 20)

    def diagnosticar(self):
        """Executa diagnóstico completo"""
        
        # PASSO 1: Acessar painel
        print("\n" + "="*70)
        print("PASSO 1: ACESSANDO PAINEL")
        print("="*70)
        url = input("🔗 Digite a URL do painel anterior: ").strip()
        
        self.driver.get(url)
        time.sleep(10)
        print("✅ Painel carregado")
        
        # PASSO 2: Verificar iFrame
        print("\n" + "="*70)
        print("PASSO 2: VERIFICANDO iFrame")
        print("="*70)
        try:
            iframes = self.driver.find_elements(By.CSS_SELECTOR, "iframe")
            print(f"✅ Encontrados {len(iframes)} iframes")
            
            if len(iframes) > 0:
                iframe = iframes[0]
                self.driver.switch_to.frame(iframe)
                print("✅ Entrou no iFrame")
            else:
                print("⚠️ Nenhum iFrame encontrado - painel pode não usar PowerBI")
        except Exception as e:
            print(f"❌ Erro: {e}")
        
        # PASSO 3: Explorar elementos visíveis
        print("\n" + "="*70)
        print("PASSO 3: ELEMENTOS VISÍVEIS NA TELA")
        print("="*70)
        
        # Procurar por "Meta X"
        print("\n📌 Buscando por 'Meta' na página...")
        try:
            elementos_meta = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Meta')]")
            print(f"✅ Encontrados {len(elementos_meta)} elementos com 'Meta':")
            for i, elem in enumerate(elementos_meta[:10]):  # Limita a 10
                texto = elem.text[:60]
                tag = elem.tag_name
                classes = elem.get_attribute("class")
                print(f"   [{i}] <{tag} class='{classes}'> → {texto}")
        except Exception as e:
            print(f"❌ Erro: {e}")
        
        # Procurar por DIVs com title attribute
        print("\n📌 Buscando por DIVs com atributo 'title'...")
        try:
            divs_title = self.driver.find_elements(By.XPATH, "//div[@title]")
            print(f"✅ Encontrados {len(divs_title)} divs com 'title':")
            título_set = set()
            for elem in divs_title[:20]:
                title = elem.get_attribute("title")
                if title and len(title) > 0:
                    título_set.add(title)
            
            for título in sorted(título_set):
                print(f"   • {título}")
        except Exception as e:
            print(f"❌ Erro: {e}")
        
        # Procurar por Cards/Cartões
        print("\n📌 Buscando por Cards/Cartões...")
        try:
            # Estratégia 1: Procura por div com classe 'card'
            cards = self.driver.find_elements(By.CSS_SELECTOR, "[class*='card'], [class*='Card']")
            print(f"✅ Encontrados {len(cards)} elementos com 'card' na classe")
            
            # Estratégia 2: Procura por div com class='textbox'
            textboxes = self.driver.find_elements(By.CSS_SELECTOR, "div.textbox")
            print(f"✅ Encontrados {len(textboxes)} elementos com class='textbox'")
            
            # Estratégia 3: Procura por visual-modern (PowerBI)
            visuals = self.driver.find_elements(By.CSS_SELECTOR, "visual-modern")
            print(f"✅ Encontrados {len(visuals)} elementos 'visual-modern' (PowerBI)")
            
        except Exception as e:
            print(f"❌ Erro: {e}")
        
        # PASSO 4: Explorar Filtros PowerBI
        print("\n" + "="*70)
        print("PASSO 4: FILTROS PowerBI")
        print("="*70)
        try:
            filtros = self.driver.find_elements(By.CSS_SELECTOR, "[class*='slicer']")
            print(f"✅ Encontrados {len(filtros)} elementos com 'slicer':")
            
            for i, filtro in enumerate(filtros[:10]):
                aria_label = filtro.get_attribute("aria-label")
                class_name = filtro.get_attribute("class")
                print(f"   [{i}] aria-label='{aria_label}' | class='{class_name}'")
        except Exception as e:
            print(f"❌ Erro: {e}")
        
        # PASSO 5: Explorar Gráficos (SVG)
        print("\n" + "="*70)
        print("PASSO 5: GRÁFICOS (SVG)")
        print("="*70)
        try:
            svgs = self.driver.find_elements(By.CSS_SELECTOR, "svg")
            print(f"✅ Encontrados {len(svgs)} SVGs (gráficos)")
            
            # Procurar por <g> com aria-label (séries)
            series = self.driver.find_elements(By.XPATH, "//*[name()='g' and @aria-label]")
            print(f"✅ Encontrados {len(series)} séries (g com aria-label):")
            
            labels_unicos = set()
            for serie in series[:30]:
                label = serie.get_attribute("aria-label")
                if label:
                    labels_unicos.add(label)
            
            for label in sorted(labels_unicos):
                print(f"   • {label}")
        except Exception as e:
            print(f"❌ Erro: {e}")
        
        # PASSO 6: Explorar Botões
        print("\n" + "="*70)
        print("PASSO 6: BOTÕES & CONTROLES")
        print("="*70)
        try:
            # Botões laranjas (cor #e1874d)
            botoes_laranja = self.driver.find_elements(By.XPATH, "//*[contains(@fill, 'e1874d')]")
            print(f"✅ Encontrados {len(botoes_laranja)} botões laranjas (#e1874d)")
            
            # Buttons em geral
            buttons = self.driver.find_elements(By.CSS_SELECTOR, "button, [role='button']")
            print(f"✅ Encontrados {len(buttons)} buttons")
        except Exception as e:
            print(f"❌ Erro: {e}")
        
        # PASSO 7: Estrutura Hierárquica (primeira Meta encontrada)
        print("\n" + "="*70)
        print("PASSO 7: ESTRUTURA HIERÁRQUICA (Primeira Meta)")
        print("="*70)
        try:
            primeiro_meta = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Meta')]")
            print(f"✅ Primeira Meta encontrada: {primeiro_meta.text[:50]}")
            print(f"   Tag: {primeiro_meta.tag_name}")
            print(f"   Classes: {primeiro_meta.get_attribute('class')}")
            print(f"   IDs: {primeiro_meta.get_attribute('id')}")
            
            # Procura ancestrais
            print(f"\n   🔍 Ancestrais:")
            ancestor = primeiro_meta
            nivel = 0
            while ancestor and nivel < 5:
                tag = ancestor.tag_name
                class_attr = ancestor.get_attribute("class")
                print(f"   {'  ' * nivel}└─ <{tag} class='{class_attr}'> ")
                ancestor = self.driver.find_element(By.XPATH, f"ancestor::{tag}[1]") if nivel < 4 else None
                nivel += 1
        except Exception as e:
            print(f"❌ Erro: {e}")
        
        # PASSO 8: Exportar HTML da Meta 1
        print("\n" + "="*70)
        print("PASSO 8: SALVAR HTML PARA ANÁLISE")
        print("="*70)
        try:
            html_content = self.driver.page_source
            with open("diagnostico_painel.html", "w", encoding="utf-8") as f:
                f.write(html_content)
            print("✅ HTML salvo em: diagnostico_painel.html")
            print("   Abra este arquivo no navegador para analisar a estrutura!")
        except Exception as e:
            print(f"❌ Erro: {e}")
        
        # RESUMO
        print("\n" + "="*70)
        print("📋 PRÓXIMOS PASSOS:")
        print("="*70)
        print("""
1. Abra 'diagnostico_painel.html' em um navegador
2. Use Ctrl+F para procurar por:
   - "Meta 1", "Meta 2", etc.
   - "aria-label" (para filtros e séries)
   - "@title" (para cards)
3. Use DevTools (F12) no Chrome para:
   - Inspecionar elementos específicos
   - Testar seletores no console
4. Envie as descobertas para que eu customize o script!
        """)
        
        input("\n⏸️ Pressione ENTER para fechar o navegador e encerrar...")
        self.driver.quit()

if __name__ == "__main__":
    diag = DiagnosticoPainel()
    diag.diagnosticar()
