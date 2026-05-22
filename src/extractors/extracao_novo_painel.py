from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import datetime
import pandas as pd
from selenium.common.exceptions import TimeoutException

# ============================================================================
# TEMPLATE PARAMETERIZADO - CÓPIA DO extracao_cnj.py
# ============================================================================
# INSTRUÇÕES DE CUSTOMIZAÇÃO:
# 1. Altere a classe de 'AutomacaoPainelCNJ' para um nome descritivo
#    (ex: 'AutomacaoPainelJusticaNumerosAlternativo', 'AutomacaoPainelDados')
#
# 2. No método acessar_painel(), altere a URL para o novo painel:
#    self.driver.get("NOVA_URL_AQUI")
#
# 3. Ajuste os nomes dos filtros e elementos conforme a estrutura do novo painel
#
# 4. Customize os métodos de extração (extrair_kpi_*, extrair_dados_da_aba, etc.)
#    according to the new dashboard structure
#
# 5. Altere o nome do arquivo de saída em salvar_excel() se necessário
#
# 6. No main, instancie a classe com o novo nome
# ============================================================================

class AutomacaoPainelNovo:
    """
    Automação para coleta de dados de novo painel.
    
    CONFIGURAÇÃO NECESSÁRIA:
    - URL_BASE: Defina a URL do novo painel
    - ARQUIVO_SAIDA: Defina o caminho/nome do arquivo Excel de saída
    - Adapte os seletores XPath, CSS e aria-labels para o novo painel
    """
    
    # ========== CONFIGURAÇÃO DO PAINEL ==========
    URL_BASE = "https://app.powerbi.com/view?r=eyJrIjoiNmI3ZGE1ZDUtMjVlYi00ZGRjLWJkZWMtZDFiYTk2OWEzMWJkIiwidCI6ImFkOTE5MGU2LWM0NWQtNDYwMC1iYzVjLWVjYTU1NGNjZjQ5NyIsImMiOjJ9"
    ARQUIVO_SAIDA = "exports/resultados_novo_painel.xlsx"
    
    def __init__(self):
        print("Inicializando robô...")
        opcoes = webdriver.ChromeOptions()
        opcoes.add_argument('--start-maximized')
        opcoes.add_argument('--disable-notifications')
        
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=opcoes
        )
        self.wait = WebDriverWait(self.driver, 20)
        self.dados_extraidos = []


    def acessar_painel(self):
        """
        Acessa o novo painel.
        
        TODO: Altere a URL e adicione lógica de autenticação se necessário
        """
        print("Acessando novo painel...")
        self.driver.get(self.URL_BASE)
        time.sleep(10)
        
        # Se necessário autenticação, adicione aqui:
        # print("Aguardando autenticação manual...")
        # input("Pressione ENTER após autenticar no navegador...")


    def entrar_no_iframe(self):
        """
        Entra no iFrame do painel (se aplicável).
        
        TODO: Adapte para o novo painel - nem todos os painéis usam iFrame
        """
        try:
            iframe = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe")))
            self.driver.switch_to.frame(iframe)
            print("✅ Entrou no contexto do Iframe")
        except:
            print("⚠️ Iframe não encontrado (painel pode não usar iframe).")


    def clicar_elemento_por_texto(self, texto_parcial):
        """
        Clica em um elemento identificado por texto parcial.
        
        Reutilizado da versão CNJ sem alterações.
        """
        print(f"Procurando elemento com texto: '{texto_parcial}'...")
        try:
            xpath = f"//*[contains(text(), '{texto_parcial}')]"
            elementos = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
            elemento_alvo = elementos[-1] 
            
            self.driver.execute_script("arguments[0].scrollIntoView(true);", elemento_alvo)
            time.sleep(0.5)
            self.driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('click', {view: window, bubbles:true, cancelable: true}))", elemento_alvo)
            
            print(f"✅ Clique em '{texto_parcial}' realizado com sucesso!")
            time.sleep(4)
            return True
        except Exception as e:
            print(f"❌ Não foi possível clicar em '{texto_parcial}'.")
            return False


    def aplicar_filtro_powerbi(self, nome_interno_filtro, valor_desejado):
        """
        Aplica um filtro em componente PowerBI.
        
        TODO: Se o painel não usa PowerBI, adapte a lógica para o framework usado
        (ex: FiltersJS, Tableau, Google Data Studio, etc.)
        """
        print(f"--- Filtrando '{nome_interno_filtro}' para '{valor_desejado}' ---")
        try:
            dropdown_xpath = f"//div[@class='slicer-dropdown-menu' and @aria-label='{nome_interno_filtro}']"
            dropdown = self.wait.until(EC.presence_of_element_located((By.XPATH, dropdown_xpath)))
            
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dropdown)
            self.wait.until(EC.element_to_be_clickable((By.XPATH, dropdown_xpath)))
            time.sleep(1)
            
            self.driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('click', {view: window, bubbles:true, cancelable: true}))", dropdown)
            time.sleep(1.5)

            opcao_xpath = f"//div[@class='slicerItemContainer']//span[@title='{valor_desejado}' or text()='{valor_desejado}']"
            opcao = self.wait.until(EC.element_to_be_clickable((By.XPATH, opcao_xpath)))
            self.driver.execute_script("arguments[0].click();", opcao)
            print(f"✅ Opção '{valor_desejado}' selecionada!")
            
            self.driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('click', {view: window, bubbles:true, cancelable: true}))", dropdown)
            time.sleep(2)
            
        except Exception as e:
            print(f"❌ Erro ao filtrar {nome_interno_filtro}: {e}")


    def adicionar_linha(self, titulo, subtitulo, desc, cat, val):
        """
        Adiciona uma linha de dados extraída.
        
        Mantém compatibilidade com o formato original do CNJ.
        Customize os nomes das colunas conforme necessário.
        """
        print(f"   > Capturado: {cat} -> {val} (Sub: {subtitulo})")
        
        partes_texto = []
        if subtitulo and subtitulo != "N/D":
            partes_texto.append(str(subtitulo).strip())
        if desc:
            partes_texto.append(str(desc).strip())
        
        texto_final = " - ".join(partes_texto) if partes_texto else "Sem descrição"

        self.dados_extraidos.append({
            "Meta": titulo,
            "Descrição Completa": texto_final,
            "Categoria": cat,
            "Resultado": val,
            "Data": datetime.now().strftime("%Y-%m-%d %H:%M")
        })


    # ========== MÉTODO EXEMPLO 1: Extração Simples (KPI - Uma Métrica) ==========
    def extrair_kpi_simples(self, numero_meta, nome_kpi=""):
        """
        Exemplo: Extrai um único valor/métrica de um card (KPI).
        
        Adaptado para o novo painel que usa <transform> com aria-label
        """
        print(f"\n--- Extração KPI Simples (Meta {numero_meta}) ---")
        
        titulo_meta = f"Meta {numero_meta}"
        subtitulo_meta = "Métrica Principal"
        descricao_meta = "Descrição não configurada"
        
        try:
            # ✅ CORRIGIDO: Novo painel usa <transform> com aria-label, não div[@title]
            if nome_kpi:
                xpath_card = f"//transform[@aria-label='{nome_kpi}']"
            else:
                xpath_card = f"//transform[contains(@aria-label, 'Meta {numero_meta}')]"
            
            card = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath_card)))
            
            # ✅ CORRIGIDO: Buscar em text.value > tspan
            valor = card.find_element(By.CSS_SELECTOR, "text.value tspan").text.strip()
            
            print(f"💎 Valor encontrado (Meta {numero_meta}): {valor}")
            self.adicionar_linha(titulo_meta, subtitulo_meta, descricao_meta, "Total", valor)
            
        except Exception as e:
            print(f"❌ Erro ao extrair KPI Meta {numero_meta}: {e}")


    # ========== MÉTODO EXEMPLO 2: Extração de Gráfico (Múltiplos Valores) ==========
    def extrair_dados_grafico(self, numero_meta, nome_serie="", titulo_grafico=""):
        """
        Exemplo: Extrai múltiplos valores de um gráfico/série.
        
        ✅ ADAPTADO: Novo painel já possui rótulos formatados em tspan
        """
        print(f"\n--- Extração Gráfico (Meta {numero_meta}) ---")
        
        titulo_meta = f"Meta {numero_meta}"
        subtitulo_meta = "N/D"
        descricao_meta = "Gráfico Detalhado"
        
        try:
            # ✅ CORRIGIDO: Buscar pelo título do gráfico
            if titulo_grafico:
                xpath_container = f"//h3[contains(text(), '{titulo_grafico}')]/ancestor::div[contains(@class, 'visualWrapper')]"
            else:
                xpath_container = f"//h3[contains(text(), 'Meta {numero_meta}')]/ancestor::div[contains(@class, 'visualWrapper')]"
            
            container_grafico = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath_container)))
            
            # ✅ CORRIGIDO: Se houver nome_serie específico, usar; senão buscar a primeira série
            if nome_serie:
                xpath_serie = f".//g[@aria-label='{nome_serie}']"
            else:
                xpath_serie = f".//g[@class='series']"
            
            serie = container_grafico.find_element(By.XPATH, xpath_serie)
            
            # ✅ CORRIGIDO: Procurar pelos rótulos formatados em label-tspan
            # Isso é mais seguro que usar aria-label das barras (que são decimais)
            labels = serie.find_elements(By.XPATH, ".//tspan[@class='label-tspan']")
            
            print(f"   > Encontrados {len(labels)} rótulos formatados")
            
            # ✅ CORRIGIDO: Os rótulos já estão formatados em tspan
            for i, label_elem in enumerate(labels):
                valor_formatado = label_elem.text.strip()  # Ex: "123,47%"
                
                # TODO: Customize a categorização
                # Você precisa mapear a ordem visual do seu gráfico
                categoria = f"Categoria {i+1}"
                
                if valor_formatado:
                    print(f"   💎 {categoria}: {valor_formatado}")
                    self.adicionar_linha(titulo_meta, subtitulo_meta, descricao_meta, categoria, valor_formatado)
        
        except Exception as e:
            print(f"❌ Erro ao extrair gráfico da Meta {numero_meta}: {e}")


    # ========== MÉTODO EXEMPLO 3: Extração Múltipla (Vários Cards) ==========
    def extrair_multiplos_cards(self, lista_cards):
        """
        Exemplo: Extrai valores de múltiplos cards em sequência.
        
        Args:
            lista_cards: Lista de tuplas (titulo_card, campo_saida)
        
        TODO: Customize conforme a estrutura do novo painel
        """
        print(f"\n--- Extração de {len(lista_cards)} Cards ---")
        
        for titulo_card, campo_saida in lista_cards:
            try:
                # TODO: Customize o seletor para seu painel
                xpath_card = f"//div[@title='{titulo_card}']"
                card = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath_card)))
                
                # TODO: Altere o seletor que lê o valor
                valor = card.find_element(By.CSS_SELECTOR, ".value").text.strip()
                
                print(f"   💎 {campo_saida}: {valor}")
                self.adicionar_linha("Meta Genérica", "N/D", titulo_card, campo_saida, valor)
                
            except Exception as e:
                print(f"   ⚠️ Erro ao extrair '{titulo_card}': {e}")


    # ========== FLUXO PRINCIPAL ==========
    def executar(self):
        """
        Fluxo principal de automação.
        
        ✅ ADAPTADO para novo painel com <transform> e rótulos em tspan
        """
        print("\n" + "="*60)
        print("INICIANDO AUTOMAÇÃO DE COLETA DE DADOS")
        print("="*60)
        
        try:
            self.acessar_painel()
            
            # ✅ META 1 CORRIGIDA
            print("\n=== 🏁 INICIANDO META 1 ===")
            
            # 1. Clicar em Meta 1 (se necessário)
            # self.clicar_elemento_por_texto("Meta 1")
            
            # 2. Aplicar filtros
            self.aplicar_filtro_powerbi("ramo_justica", "Justiça Estadual")
            time.sleep(2)
            
            # 3. Extrair gráfico
            self.extrair_dados_grafico(
                numero_meta=1, 
                nome_serie="Cumprimento meta 1",
                titulo_grafico="Meta 1 por Ramo"
            )
            
            # 4. Extrair KPI
            self.extrair_kpi_simples(
                numero_meta=1, 
                nome_kpi="Julgar mais processos que os distribuídos"
            )
            
            # TODO: Descomentar e adaptar outras metas conforme necessário
            # print("\n=== 🏁 INICIANDO META 2 ===")
            # self.clicar_elemento_por_texto("Meta 2")
            # ...
            
        except Exception as e:
            print(f"\n❌ Erro geral na automação: {e}")
        
        finally:
            print("\n⏸️ Processo finalizado.")
            self.salvar_excel()
            input("\nPressione ENTER para fechar o navegador e encerrar o robô...")
            self.driver.quit()


    def salvar_excel(self):
        """
        Salva os dados extraídos em um arquivo Excel.
        
        TODO: Customize o caminho/nome do arquivo conforme necessário
        """
        if self.dados_extraidos:
            df = pd.DataFrame(self.dados_extraidos)
            arquivo = self.ARQUIVO_SAIDA
            df.to_excel(arquivo, index=False)
            print(f"\n✅ Arquivo salvo: {arquivo}")
        else:
            print("\n⚠️ Nenhum dado para salvar.")


# ============================================================================
# PONTO DE ENTRADA
# ============================================================================

if __name__ == "__main__":
    print("\n📋 TEMPLATE DE AUTOMAÇÃO - COLETA DE NOVO PAINEL")
    print("="*60)
    print("\n⚠️  ANTES DE EXECUTAR:")
    print("1. Configure a URL_BASE na classe AutomacaoPainelNovo")
    print("2. Customize os seletores XPath/CSS para seu painel")
    print("3. Adapte os métodos de extração conforme necessário")
    print("4. Verifique se o iFrame é necessário")
    print("\n" + "="*60 + "\n")
    
    robo = AutomacaoPainelNovo()
    robo.executar()
