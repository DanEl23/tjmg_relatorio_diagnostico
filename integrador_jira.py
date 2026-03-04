"""
EXTRATOR JIRA - TJMG
Versão: 3.6 (Integração de Extração Universal + Módulo 3 + Pausa Global)
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import time
import traceback
import re
import json
import sys
from urllib.parse import quote_plus
from pathlib import Path

# ============================================
# CONFIGURAÇÕES GLOBAIS
# ============================================

class Config:
    URL_JIRA = "https://tjmg.atlassian.net/"
    JQL_BASE = "project = ASPLAGMETA ORDER BY created DESC"
    ANOS_EXTRACAO = ["2022", "2023", "2024", "2025", "2026"]
    
    PASTA_SAIDA = Path("exports")
    ARQUIVO_JIRA_SIMPLES = "dados_exportados_jira.xlsx"
    ARQUIVO_JIRA_ANUAL = "dados_exportados_jira_por_ano.xlsx"
    ARQUIVO_METAS_DETALHADO = "dados_detalhados_metas_2025.xlsx"
    
    NAVEGADOR = "edge" 
    TIMEOUT = 25

# ============================================
# EXTRATOR JIRA
# ============================================

class ExtratorJira:
    def __init__(self, config=None):
        self.config = config or Config()
        self.driver = None
        self.wait = None
        self.dados_extraidos = []
        self.janela_principal = None
        
    def iniciar_navegador(self):
        print(f"🌐 Iniciando {self.config.NAVEGADOR.upper()}...")
        opts = webdriver.EdgeOptions() if self.config.NAVEGADOR == "edge" else webdriver.ChromeOptions()
        opts.add_argument('--start-maximized')
        opts.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        if self.config.NAVEGADOR == "edge":
            self.driver = webdriver.Edge(options=opts)
        else:
            self.driver = webdriver.Chrome(options=opts)
            
        self.wait = WebDriverWait(self.driver, self.config.TIMEOUT)
        print("\n" + "!"*60)
        print("💡 DICA: Pressione [CTRL + C] no terminal para PAUSAR a qualquer momento.")
        print("!"*60)

    def menu_pausa(self):
        print("\n" + "="*50 + "\n🛑 AUTOMAÇÃO PAUSADA PELO USUÁRIO\n" + "="*50)
        print("O navegador está livre para verificação.")
        print("\nOpções: [ENTER] Continuar | [S] Sair")
        if input("\nEscolha: ").strip().lower() == 's':
            self.fechar()
            sys.exit(0)
        print("▶️ Retomando...")

    def safe_run(self, func, *args, **kwargs):
        while True:
            try: return func(*args, **kwargs)
            except KeyboardInterrupt: self.menu_pausa()
            except Exception as e:
                print(f"❌ Erro em {func.__name__}: {e}")
                if input("Tentar novamente? (s/n): ").lower() != 's': raise e

    def fechar(self):
        if self.driver: self.driver.quit()

    def login_manual(self):
        self.driver.get(self.config.URL_JIRA)
        print("\n🔐 Faça o login e pressione ENTER no terminal...")
        input()
        self.janela_principal = self.driver.current_window_handle

    # --- FLUXO DE NAVEGAÇÃO ---

    def exportar_detalhes_impressao(self):
        """Abre o menu de exportação e aguarda a nova aba."""
        print("\n⚙️  Exportando via Meatball Menu...")
        try:
            # 1. Meatball Menu (...)
            btn_mais = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='issue-navigator-action-meatball-menu.ui.menu-trigger']")))
            self.driver.execute_script("arguments[0].click();", btn_mais)
            time.sleep(1)
            
            # 2. Export
            btn_export = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='issue-navigator-action-export-issues.ui.filter-button--trigger']")))
            self.driver.execute_script("arguments[0].click();", btn_export)
            time.sleep(1)
            
            # 3. Link Detalhes de Impressão
            xpath_print = "//a[@role='menuitem' and .//div[text()='Detalhes de impressão']] | //span[contains(text(), 'Detalhes de impressão')]"
            opcao_print = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath_print)))
            
            wins_antes = self.driver.window_handles
            self.driver.execute_script("arguments[0].click();", opcao_print)
            
            WebDriverWait(self.driver, 25).until(lambda d: len(d.window_handles) > len(wins_antes))
            time.sleep(3)
            return True
        except Exception as e:
            print(f"❌ Erro na exportação: {e}")
            self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
            return False

    # --- SUA FUNÇÃO DE EXTRAÇÃO REGISTRADA ---

    def processar_aba_exportacao(self):
        """
        Extração Universal com Lógica de Herança (Versão Fornecida pelo Usuário).
        """
        janelas = self.driver.window_handles
        if len(janelas) < 2:
            print("❌ Nova aba de exportação não detectada")
            return 0
        
        janela_exportacao = [w for w in janelas if w != self.janela_principal][0]
        self.driver.switch_to.window(janela_exportacao)
        print("\n🔄 Foco mudado para aba de exportação. Processando conteúdo...")
        
        html_content = self.driver.page_source
        start_time = time.time()
        
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            blocos_tickets = soup.find_all('table', class_='tableBorder')
            num_tickets = len(blocos_tickets)
            print(f"📊 Encontrados {num_tickets} tickets para processamento.")
            
            for idx, tabela_inicio in enumerate(blocos_tickets):
                registro = {}
                
                parent_key_tag = tabela_inicio.find('a', id='parent_issue_key')
                registro['META_ID'] = parent_key_tag.get_text(strip=True) if parent_key_tag else ""
                
                parent_summary_tag = tabela_inicio.find('a', id='parent_issue_summary')
                nome_meta_pai = parent_summary_tag.get_text(strip=True) if parent_summary_tag else ""
                registro['Nº_Meta'] = nome_meta_pai
                
                h3_element = tabela_inicio.find('h3', class_='formtitle')
                if h3_element:
                    titulo_texto = h3_element.get_text(separator=' ', strip=True)
                    chave_match = re.search(r'\[([A-Z]+-\d+)\]', titulo_texto)
                    current_chave = chave_match.group(1) if chave_match else f"TICKET-{idx+1}"
                    registro['Chave'] = current_chave
                    
                    resumo_link = h3_element.find('a')
                    resumo_original = resumo_link.get_text(strip=True) if resumo_link else ""
                    
                    if "Apurado no período" in resumo_original:
                        registro['Resumo'] = f"Apuração: {nome_meta_pai}"
                        registro['Apurado no período'] = resumo_original 
                    else:
                        registro['Resumo'] = resumo_original
                    
                    registro['Meta_apuração'] = f"[{current_chave}] {registro['Resumo']}"

                current_element = tabela_inicio
                while current_element:
                    if current_element.name == 'table':
                        for linha in current_element.find_all('tr'):
                            celulas = linha.find_all(['td', 'th'])
                            for c_idx, celula in enumerate(celulas):
                                b_tag = celula.find('b')
                                if b_tag and (c_idx + 1) < len(celulas):
                                    rotulo = re.sub(r'\s+', ' ', b_tag.get_text(strip=True).rstrip(':')).strip()
                                    if rotulo in ['Chave', 'Resumo', 'Tipo']:
                                        continue 
                                    valor_td = celulas[c_idx + 1]
                                    
                                    time_tag = valor_td.find('time')
                                    if time_tag and time_tag.get('datetime'):
                                        valor = time_tag['datetime']
                                    elif rotulo.lower() == 'informação complementar':
                                        valor = valor_td.decode_contents().strip()
                                    else:
                                        valor = valor_td.get_text(separator=' ', strip=True)
                                    
                                    if valor and valor.lower() != "desconhecido":
                                        registro[rotulo] = valor
                    
                    proximo = current_element.find_next_sibling()
                    if not proximo or (proximo.name == 'hr' and 'fullcontent' in proximo.get('class', [])):
                        break
                    current_element = proximo
                
                if registro.get('Chave'):
                    self.dados_extraidos.append(registro)
            
            elapsed = time.time() - start_time
            print(f"✅ Extração finalizada em {elapsed:.2f}s.")
            
        except Exception as e:
            print(f"❌ Erro crítico na extração: {e}")
            traceback.print_exc()
        finally:
            self.driver.close()
            self.driver.switch_to.window(self.janela_principal)
            print("↩️  Retornando à aba de controle do Jira.")
            return num_tickets

    # --- MODOS DE OPERAÇÃO ---

    def run_simples(self):
        self.iniciar_navegador()
        self.safe_run(self.login_manual)
        self.safe_run(self.driver.get, f"{self.config.URL_JIRA}issues/?jql={quote_plus(self.config.JQL_BASE)}")
        if self.safe_run(self.exportar_detalhes_impressao):
            self.safe_run(self.processar_aba_exportacao)
        self.salvar_dados(self.config.ARQUIVO_JIRA_SIMPLES)

    def run_anual(self):
        self.iniciar_navegador()
        self.safe_run(self.login_manual)
        for ano in self.config.ANOS_EXTRACAO:
            print(f"📅 Processando Ano: {ano}")
            jql = f'project = ASPLAGMETA AND "Ano da Meta" = {ano} ORDER BY created DESC'
            self.safe_run(self.driver.get, f"{self.config.URL_JIRA}issues/?jql={quote_plus(jql)}")
            if self.safe_run(self.exportar_detalhes_impressao):
                self.safe_run(self.processar_aba_exportacao)
        self.salvar_dados(self.config.ARQUIVO_JIRA_ANUAL)

    def run_detalhado_metas_2025(self):
        print("\n🔍 Módulo 3: Extração Detalhada Metas 2025")
        caminho_anual = self.config.PASTA_SAIDA / self.config.ARQUIVO_JIRA_ANUAL
        if not caminho_anual.exists():
            print("❌ Erro: O arquivo do Módulo 2 não foi encontrado.")
            return

        df = pd.read_excel(caminho_anual)
        # Identificação dinâmica da coluna Ano
        col_ano = [c for c in df.columns if 'Ano da Meta' in c][0]
        mask = df[col_ano].astype(str).str.contains('2025', na=False)
        metas_list = df.loc[mask, 'Resumo'].str.extract(r'(TJMG\s+\d+)', expand=False).dropna().unique().tolist()

        if not metas_list:
            print("⚠️ Nenhuma meta TJMG encontrada para 2025.")
            return

        self.iniciar_navegador()
        self.safe_run(self.login_manual)

        for meta in metas_list:
            print(f"🚀 Buscando detalhes: {meta}")
            query = f'project = ASPLAGMETA AND (summary ~ "{meta}*" OR summary ~ "{meta}") ORDER BY created DESC'
            self.safe_run(self.driver.get, f"{self.config.URL_JIRA}issues/?jql={quote_plus(query)}")
            if self.safe_run(self.exportar_detalhes_impressao):
                self.safe_run(self.processar_aba_exportacao)

        self.salvar_dados(self.config.ARQUIVO_METAS_DETALHADO)

    def salvar_dados(self, nome_arquivo):
        if self.dados_extraidos:
            self.config.PASTA_SAIDA.mkdir(exist_ok=True)
            pd.DataFrame(self.dados_extraidos).to_excel(self.config.PASTA_SAIDA / nome_arquivo, index=False)
            print(f"💾 Arquivo salvo: {nome_arquivo}")
            self.dados_extraidos = []
        self.fechar()

# ============================================
# INTERFACE
# ============================================

if __name__ == "__main__":
    while True:
        print("\n" + "="*40 + "\n🎯 EXTRATOR JIRA v3.6\n" + "="*40)
        print("1. Extração Simples")
        print("2. Extração Anual")
        print("3. Extração Detalhada Metas 2025")
        print("0. Sair")
        
        opt = input("\nEscolha: ").strip()
        if opt == "0": break
        elif opt == "1": ExtratorJira().run_simples()
        elif opt == "2": ExtratorJira().run_anual()
        elif opt == "3": ExtratorJira().run_detalhado_metas_2025()