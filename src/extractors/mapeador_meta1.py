import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MapeadorAvancado:
    def __init__(self):
        print("🕵️‍♂️ INICIANDO MAPEAMENTO AVANÇADO DE TIPOS VISUAIS")
        options = webdriver.EdgeOptions()
        # options.add_argument("--headless") # Recomendo deixar visual para ver o progresso
        options.add_argument('--start-maximized')
        options.add_argument('--disable-blink-features=AutomationControlled')
        
        self.driver = webdriver.Edge(options=options)
        self.wait = WebDriverWait(self.driver, 20)
        self.URL = "https://justica-em-numeros.cnj.jus.br/painel-metas/"

    def detectar_tipo_visual(self, container):
        """
        Analisa o HTML interno do container para descobrir o tipo de visualização.
        """
        html_interno = container.get_attribute('innerHTML')
        classes = container.get_attribute('class')
        
        tipo = "DESCONHECIDO"
        confianca = "Baixa"

        # 1. Tentar identificar pela classe do visual-modern (Padrão PowerBI)
        try:
            visual_modern = container.find_element(By.TAG_NAME, "visual-modern")
            # Procura div interna com classe específica
            if visual_modern.find_elements(By.CSS_SELECTOR, ".visual-barChart") or \
               visual_modern.find_elements(By.CSS_SELECTOR, ".visual-columnChart") or \
               visual_modern.find_elements(By.CSS_SELECTOR, ".visual-clusteredBarChart"):
                return "📊 GRÁFICO DE BARRAS/COLUNAS", "Alta"
            
            if visual_modern.find_elements(By.CSS_SELECTOR, ".visual-lineChart") or \
               visual_modern.find_elements(By.CSS_SELECTOR, ".visual-areaChart"):
                return "📈 GRÁFICO DE LINHAS/ÁREA", "Alta"
            
            if visual_modern.find_elements(By.CSS_SELECTOR, ".visual-card") or \
               visual_modern.find_elements(By.CSS_SELECTOR, ".visual-multiRowCard"):
                return "🃏 CARTÃO NUMÉRICO (KPI)", "Alta"
                
            if visual_modern.find_elements(By.CSS_SELECTOR, ".visual-slicer"):
                return "🔽 FILTRO (SLICER)", "Alta"
        except:
            pass

        # 2. Heurística por Tags SVG (Caso o método acima falhe)
        if "visual-barChart" in html_interno or "ClusteredBarChart" in html_interno:
            return "📊 GRÁFICO DE BARRAS (Inferido)", "Média"
        
        if "visual-lineChart" in html_interno or "LineChart" in html_interno:
            return "📈 GRÁFICO DE LINHAS (Inferido)", "Média"
            
        if "visual-card" in html_interno or "Card" in html_interno:
            return "🃏 CARTÃO (Inferido)", "Média"

        # 3. Heurística por elementos gráficos brutos
        try:
            svgs = container.find_elements(By.TAG_NAME, "svg")
            if svgs:
                # Se tem muitos rectangles, provavel barra
                rects = container.find_elements(By.TAG_NAME, "rect")
                if len(rects) > 5:
                    return "📊 GRÁFICO (Genérico - Barras?)", "Baixa"
                
                # Se tem paths complexos e eixo, provavel linha
                paths = container.find_elements(By.TAG_NAME, "path")
                if len(paths) > 2 and "axis" in html_interno:
                    return "📈 GRÁFICO (Genérico - Linhas?)", "Baixa"
                
                # Se tem texto 'value' grande
                vals = container.find_elements(By.CSS_SELECTOR, "text.value")
                if vals:
                    return "🃏 CARTÃO (Genérico)", "Baixa"
        except: pass

        # 4. Texto Simples
        if "textbox" in classes or "image" in classes:
            return "📝 TEXTO/IMAGEM", "Alta"

        return tipo, confianca

    def extrair_titulo(self, container):
        """Tenta encontrar o título do gráfico/card."""
        try:
            # Tentativa 1: H3 direto (Muitos usam isso)
            h3 = container.find_elements(By.TAG_NAME, "h3")
            if h3 and h3[0].text.strip():
                return h3[0].text.strip()
            
            # Tentativa 2: visualTitle
            vtitle = container.find_elements(By.CSS_SELECTOR, "div.visualTitle")
            if vtitle and vtitle[0].text.strip():
                return vtitle[0].text.strip()
                
            # Tentativa 3: Título via atributo title
            if container.get_attribute("title"):
                return container.get_attribute("title")
                
            return "SEM TÍTULO"
        except:
            return "ERRO TÍTULO"

    def extrair_amostra_dados(self, container):
        """Pega uma amostra de texto para ajudar na identificação."""
        texto = container.text.replace("\n", " | ")
        if len(texto) > 60:
            return texto[:60] + "..."
        return texto

    def iniciar(self):
        try:
            self.driver.get(self.URL)
            time.sleep(10)
            
            iframe = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe")))
            self.driver.switch_to.frame(iframe)
            print("✅ Conectado ao Painel.")

            # Loop de Navegação
            for pagina in range(1, 20): # Limite seguro
                # Tenta identificar nome da meta
                nome_meta = "Desconhecida"
                try:
                    textos = self.driver.find_elements(By.CSS_SELECTOR, "div.textbox, text.title")
                    for el in textos:
                        if "Meta " in el.text:
                            nome_meta = el.text.split("\n")[0] # Pega primeira linha
                            break
                except: pass

                print(f"\n{'='*80}")
                print(f"📍 PÁGINA {pagina}: {nome_meta}")
                print(f"{'='*80}")

                # --- ANÁLISE DOS ELEMENTOS ---
                containers = self.driver.find_elements(By.CSS_SELECTOR, "div.visualContainer")
                
                for i, container in enumerate(containers):
                    # Ignora containers invisíveis ou muito pequenos
                    if container.size['height'] < 10 or container.size['width'] < 10:
                        continue
                        
                    tipo, confianca = self.detectar_tipo_visual(container)
                    
                    # Filtramos apenas o que interessa (Gráficos e Cartões)
                    if "TEXTO" in tipo or "FILTRO" in tipo or "DESCONHECIDO" in tipo:
                        continue

                    titulo = self.extrair_titulo(container)
                    amostra = self.extrair_amostra_dados(container)

                    print(f"   🔹 ELEMENTO {i}:")
                    print(f"      🏷️  Título: '{titulo}'")
                    print(f"      👁️  Tipo Detectado: {tipo} (Confiança: {confianca})")
                    print(f"      📄  Amostra: {amostra}")
                    print(f"      --------------------------------------------------")

                # Navegar Próxima Página
                try:
                    btn = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Próxima Página']")
                    if btn.get_attribute("aria-disabled") == "true":
                        print("\n⛔ Fim da navegação (Última página).")
                        break
                    btn.click()
                    print("\n➡️ Indo para próxima página...")
                    time.sleep(5) # Tempo para renderizar novos gráficos
                except:
                    print("\n⚠️ Botão de próxima página não encontrado.")
                    break

        except Exception as e:
            print(f"❌ Erro Geral: {e}")
        finally:
            self.driver.quit()

if __name__ == "__main__":
    MapeadorAvancado().iniciar()