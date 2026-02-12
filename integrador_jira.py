"""
EXTRATOR & PROCESSADOR JIRA - TJMG
Versão: 3.10 (Correção de Tabelas Fantasmas e Extração Precisa)
Correções:
- Ignora tabelas de layout/subtarefas que sujavam o Excel.
- Extração precisa de Chave e Resumo baseada no HTML fornecido.
- Garante que a primeira coluna seja sempre o Ano da Meta.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time
import traceback
import re
import json
import argparse
import os
from urllib.parse import quote_plus
from datetime import datetime
from pathlib import Path


# ============================================
# 1. CONFIGURAÇÕES
# ============================================

class Config:
    URL_JIRA = "https://tjmg.atlassian.net/"
    JQL_CORE = "project = ASPLAGMETA"
    ANOS_EXTRACAO = ["2022", "2023", "2024", "2025", "2026"]
    
    PASTA_SAIDA = "exports"
    ARQUIVO_JIRA_SIMPLES = "dados_exportados_jira.xlsx"
    ARQUIVO_JIRA_ANUAL = "dados_exportados_jira_por_ano.xlsx"
    ARQUIVO_JIRA_JSON = "dicionario_metas_hierarquico.json"
    ARQUIVO_JIRA_ADAPTADO = "dados_exportados_jira_adaptado.xlsx"
    
    NAVEGADOR = "edge" 
    TIMEOUT = 30

# Mapeamento Fixo de Superintendências
META_SUPERINTENDENCIA = {
    "TJMG 1": "SUPINST", "TJMG 2": "SUPAD", "TJMG 3": "SUPAD", "TJMG 4": "SUPAD",
    "TJMG 5": "SUPAD", "TJMG 6": "SUPAD", "TJMG 7": "SUPAD", "TJMG 8": "SUPAD",
    "TJMG 9": "SUPAD", "TJMG 10": "SUPAD", "TJMG 11": "SUPAD", "TJMG 12": "SUPAD",
    "TJMG 13": "SUPAD", "TJMG 14": "SUPAD", "TJMG 15": "SUPAD", "TJMG 16": "SUPAD",
    "TJMG 17": "SUPAD", "TJMG 18": "SUPAD", "TJMG 19": "SUPINST", "TJMG 20": "SUPINST",
    "TJMG 21": "SUPINST", "TJMG 22": "SUPINST", "TJMG 23": "SUPINST", "TJMG 24": "SUPINST",
    "TJMG 25": "SUPINST", "TJMG 26": "SUPINST", "TJMG 27": "SUPINST", "TJMG 28": "SUPINST",
    "TJMG 29": "SUPINST", "TJMG 30": "SUPINST", "TJMG 31": "SUPINST", "TJMG 32": "SUPINST",
    "TJMG 33": "SUPINST", "TJMG 34": "SUPINST", "TJMG 35": "SUPINST", "TJMG 36": "SUPINST",
    "TJMG 37": "SUPINST", "TJMG 38": "SUPINST", "TJMG 39": "SUPINST", "TJMG 40": "SUPINST",
    "TJMG 41": "SUPINST", "TJMG 42": "SUPINST", "TJMG 43": "SUPINST", "TJMG 44": "SUPINST",
    "TJMG 45": "SUPJUD", "TJMG 46": "SUPJUD", "TJMG 47": "SUPJUD", "TJMG 48": "SUPJUD",
    "TJMG 49": "SUPJUD", "TJMG 50": "SUPJUD", "TJMG 51": "SUPJUD", "TJMG 52": "SUPJUD",
    "TJMG 53": "SUPJUD", "TJMG 54": "SUPJUD", "TJMG 55": "SUPJUD", "TJMG 56": "SUPJUD",
    "TJMG 57": "SUPJUD", "TJMG 58": "SUPJUD", "TJMG 59": "SUPJUD", "TJMG 60": "SUPJUD",
    "TJMG 61": "SUPJUD", "TJMG 62": "SUPJUD", "TJMG 63": "SUPJUD", "TJMG 64": "SUPJUD",
    "TJMG 65": "SUPJUD", "TJMG 66": "SUPJUD", "TJMG 67": "SUPJUD", "TJMG 68": "SUPJUD",
    "TJMG 69": "SUPJUD", "TJMG 70": "SUPJUD", "TJMG 71": "SUPJUD", "TJMG 72": "SUPJUD",
    "TJMG 73": "SUPJUD", "TJMG 74": "SUPJUD", "TJMG 75": "SUPJUD", "TJMG 76": "SUPJUD",
    "TJMG 77": "SUPJUD", "TJMG 78": "SUPJUD", "TJMG 79": "SUPJUD", "TJMG 80": "SUPJUD",
    "TJMG 81": "SUPJUD", "TJMG 82": "SUPJUD", "TJMG 83": "SUPJUD", "TJMG 84": "SUPJUD",
    "TJMG 85": "SUPJUD", "TJMG 86": "SUPJUD", "TJMG 87": "SUPJUD", "TJMG 88": "SUPJUD",
    "TJMG 89": "SUPADM", "TJMG 90": "SUPADM", "TJMG 91": "SUPADM", "TJMG 92": "SUPADM",
    "TJMG 93": "SUPADM", "TJMG 94": "SUPADM", "TJMG 95": "SUPADM", "TJMG 96": "SUPADM",
    "TJMG 97": "SUPADM", "TJMG 98": "SUPADM", "TJMG 99": "SUPADM", "TJMG 100": "SUPADM",
    "TJMG 101": "SUPADM", "TJMG 102": "SUPADM", "TJMG 103": "SUPADM", "TJMG 104": "SUPADM",
    "TJMG 105": "SUPADM", "TJMG 106": "SUPADM", "TJMG 107": "SUPADM", "TJMG 108": "SUPADM",
    "TJMG 109": "SUPADM", "TJMG 110": "SUPADM", "TJMG 111": "SUPADM", "TJMG 112": "SUPADM",
    "TJMG 113": "SUPADM", "TJMG 114": "SUPTI", "TJMG 115": "SUPTI", "TJMG 116": "SUPTI",
    "TJMG 117": "SUPTI", "TJMG 118": "SUPTI", "TJMG 119": "SUPTI", "TJMG 120": "SUPTI",
    "TJMG 121": "SUPTI", "TJMG 122": "SUPTI", "TJMG 123": "SUPTI", "TJMG 124": "SUPTI",
    "TJMG 125": "SUPEH", "TJMG 126": "SUPEH", "TJMG 127": "SUPEH", "TJMG 128": "SUPEH",
    "TJMG 129": "SUPEH", "TJMG 130": "SUPEH", "TJMG 131": "SUPEH", "TJMG 132": "SUPEH",
    "TJMG 133": "SUPEH", "TJMG 134": "SUPEH", "TJMG 135": "SUPEH", "TJMG 136": "SUPEH",
    "TJMG 137": "SUPLOG", "TJMG 138": "SUPLOG", "TJMG 139": "SUPLOG", "TJMG 140": "SUPLOG",
    "TJMG 141": "SUPLOG", "TJMG 142": "SUPLOG", "TJMG 143": "SUPLOG", "TJMG 144": "SUPLOG",
    "TJMG 145": "SUPLOG", "TJMG 146": "SUPCOM", "TJMG 147": "SUPCOM", "TJMG 148": "SUPCOM",
    "TJMG 149": "SUPCOM", "TJMG 150": "SUPCOM", "TJMG 151": "SUPCOM", "TJMG 152": "SUPCOM",
    "TJMG 153": "SUPCOM", "TJMG 154": "DIRSEP", "TJMG 155": "DIRSEP", "TJMG 156": "DIRSEP",
    "TJMG 157": "DIRSEP", "TJMG 158": "EJEF", "TJMG 159": "EJEF", "TJMG 160": "EJEF",
    "TJMG 161": "EJEF", "TJMG 162": "EJEF", "TJMG 163": "EJEF", "TJMG 164": "EJEF",
    "TJMG 165": "EJEF", "TJMG 166": "EJEF", "TJMG 167": "EJEF", "TJMG 168": "EJEF",
    "TJMG 169": "CGJ", "TJMG 170": "CGJ", "TJMG 171": "CGJ", "TJMG 172": "CGJ",
    "TJMG 173": "CGJ", "TJMG 174": "CGJ", "TJMG 175": "CGJ", "TJMG 176": "CGJ",
    "TJMG 177": "CGJ", "TJMG 178": "CGJ", "TJMG 179": "CGJ", "TJMG 180": "CGJ",
    "TJMG 181": "CGJ", "TJMG 182": "CGJ", "TJMG 183": "CGJ", "TJMG 184": "CGJ",
    "TJMG 185": "CGJ", "TJMG 186": "CGJ", "TJMG 187": "CGJ", "TJMG 188": "CGJ",
    "TJMG 189": "CGJ", "TJMG 190": "CGJ", "TJMG 191": "CGJ", "TJMG 192": "CGJ",
    "TJMG 193": "CGJ", "TJMG 194": "CGJ", "TJMG 195": "CGJ", "TJMG 196": "CGJ",
    "TJMG 197": "CGJ", "TJMG 198": "CGJ", "TJMG 199": "CGJ", "TJMG 200": "CGJ",
    "TJMG 201": "CGJ", "TJMG 202": "CGJ"
}

# ============================================
# 2. PROCESSADOR DE DADOS
# ============================================

class ProcessadorJira:
    def __init__(self, config=None):
        self.config = config or Config()

    def processar_estilo_notebook(self):
        print("\n⚙️  Iniciando PROCESSAMENTO DE DADOS...")
        path_anual = Path(self.config.PASTA_SAIDA) / self.config.ARQUIVO_JIRA_ANUAL
        path_simples = Path(self.config.PASTA_SAIDA) / self.config.ARQUIVO_JIRA_SIMPLES
        
        if not path_simples.exists():
            print(f"❌ Arquivo principal ausente: {path_simples}")
            return

        try:
            print("   📖 Lendo arquivos Excel...")
            # Garante leitura como string para evitar erros de tipo
            df_simples = pd.read_excel(path_simples, dtype=str)
            
            if path_anual.exists():
                df_anual = pd.read_excel(path_anual, dtype=str)
                if 'Chave' in df_anual.columns:
                    print("   🧹 Deduplicando base anual...")
                    df_anual = df_anual.drop_duplicates(subset=['Chave'], keep='last')
                
                print("   🔗 Enriquecendo 'Ano da Meta'...")
                if 'Chave' in df_anual.columns and 'Ano da Meta' in df_anual.columns:
                    mapa = df_anual.set_index('Chave')['Ano da Meta']
                    df_simples['Ano da Meta'] = df_simples['Chave'].map(mapa).fillna(df_simples.get('Ano da Meta'))

            print("   🌳 Propagando Ano para Apurações...")
            if 'META_ID' in df_simples.columns:
                df_simples['Ano da Meta'] = df_simples['Ano da Meta'].fillna(
                    df_simples.groupby('META_ID')['Ano da Meta'].transform(
                        lambda x: x.ffill().bfill()
                    )
                )
            
            df_final = self._aplicar_regras(df_simples)
            
            # Reordenação final: Ano deve ser o primeiro
            cols = df_final.columns.tolist()
            if 'Ano da Meta' in cols:
                cols.insert(0, cols.pop(cols.index('Ano da Meta')))
                df_final = df_final[cols]

            path_out = Path(self.config.PASTA_SAIDA) / self.config.ARQUIVO_JIRA_ADAPTADO
            df_final.to_excel(path_out, index=False)
            print(f"✅ ARQUIVO ADAPTADO PRONTO: {path_out}")
            
        except Exception as e:
            print(f"❌ Erro processamento: {e}")
            traceback.print_exc()

    def _aplicar_regras(self, df):
        df = df.copy()
        
        # Garante colunas essenciais
        for col in ['META_ID', 'Nº_Meta', 'Resumo', 'Chave']:
            if col not in df.columns: df[col] = ""

        # Lógica: Se não tem Nº_Meta (não herdou), usa o próprio Resumo
        df['Nº_Meta'] = df.apply(
            lambda row: row['Resumo'] if pd.isna(row['Nº_Meta']) or str(row['Nº_Meta']).strip() == "" else row['Nº_Meta'], 
            axis=1
        )

        # Extração de código (TJMG 123)
        def get_cod(txt):
            if not isinstance(txt, str): return None
            m = re.match(r'^([A-Z]+\s+\d+)', txt.strip())
            return m.group(1) if m else None

        df['Cod_Meta'] = df['Nº_Meta'].apply(get_cod)
        df['Superintendência'] = df['Cod_Meta'].map(lambda x: META_SUPERINTENDENCIA.get(x, "SEM CLASSIFICAÇÃO"))
        
        if 'Ano da Meta' in df.columns:
            # Converte ano para numérico para ordenar, mas mantém original no final
            df['Ano_Temp'] = pd.to_numeric(df['Ano da Meta'], errors='coerce')
            df.sort_values(by=['Ano_Temp', 'Cod_Meta'], ascending=[False, True], inplace=True)
            df.drop(columns=['Ano_Temp'], inplace=True)
            
        return df


# ============================================
# 3. EXTRATOR JIRA (Classes de Conexão)
# ============================================

class ExtratorBase:
    def __init__(self, config=None):
        self.config = config or Config()
        self.driver = None
        self.wait = None
        self.dados_extraidos = []
        self.processador = ProcessadorJira(self.config)
        
    def iniciar_navegador(self):
        print(f"🌐 Iniciando {self.config.NAVEGADOR} (Modo Blindado)...")
        if self.config.NAVEGADOR == "edge":
            opts = webdriver.EdgeOptions()
            opts.add_argument('--start-maximized')
            opts.add_argument('--ignore-certificate-errors')
            opts.add_argument('--allow-insecure-localhost')
            opts.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
            self.driver = webdriver.Edge(options=opts)
        else:
            opts = webdriver.ChromeOptions()
            opts.add_argument('--start-maximized')
            opts.add_argument('--ignore-certificate-errors')
            self.driver = webdriver.Chrome(options=opts)
        
        self.driver.set_page_load_timeout(120)
        self.wait = WebDriverWait(self.driver, self.config.TIMEOUT)
        
    def fechar(self):
        if self.driver:
            self.driver.quit()
            print("🔴 Navegador fechado")
            
    def criar_pasta_saida(self):
        Path(self.config.PASTA_SAIDA).mkdir(exist_ok=True)


class ExtratorJira(ExtratorBase):
    def __init__(self, config=None):
        super().__init__(config)
        self.janela_principal = None
        
    def login_manual_e_aguardar(self):
        try:
            self.driver.get(self.config.URL_JIRA)
            print("\n🔐 Login Manual Requerido. Pressione ENTER após logar...")
            input()
            self.janela_principal = self.driver.current_window_handle
        except Exception as e:
            print(f"⚠️ Erro ao carregar: {e}")
            input("Pressione ENTER após carregar manualmente.")
            self.janela_principal = self.driver.current_window_handle
    
    def navegar_jql(self, jql):
        print(f"➡️  JQL: {jql}")
        try:
            url = f"{self.config.URL_JIRA}issues/?jql={quote_plus(jql)}"
            self.driver.get(url)
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='issue-navigator-list']")))
        except:
            print("   ⚠️  Lista lenta. Tentando seguir...")
        time.sleep(2)

    def exportar_detalhes_impressao(self):
        print("⚙️  Exportando...")
        try:
            btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@data-testid, 'export-issues') or contains(., 'Exportar')]")))
            btn.click()
            link = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Detalhes de impressão')]")))
            wins = self.driver.window_handles
            link.click()
            WebDriverWait(self.driver, 20).until(lambda d: len(d.window_handles) > len(wins))
            time.sleep(3)
            return True
        except Exception as e:
            print(f"❌ Erro exportação: {e}")
            return False

    def processar_aba_exportacao(self):
        """
        Versão 3.10: Filtra tabelas 'fantasmas' e garante extração correta.
        """
        janelas = self.driver.window_handles
        if len(janelas) < 2: return
        self.driver.switch_to.window(janelas[-1])
        
        try:
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            # Pega todas as tabelas de borda
            todas_tabelas = soup.find_all('table', class_='tableBorder')
            
            # --- FILTRAGEM VITAL ---
            # Só aceita tabelas que tenham o cabeçalho de título (h3 class='formtitle')
            # Isso elimina tabelas de sub-tarefas e cloners que sujavam o CSV.
            tickets_reais = [t for t in todas_tabelas if t.find('h3', class_='formtitle')]
            
            print(f"   📊 Processando {len(tickets_reais)} tickets REAIS (de {len(todas_tabelas)} tabelas encontradas)...")
            
            for idx, tab in enumerate(tickets_reais):
                reg = {}
                
                # 1. Extração do Título (Chave e Resumo)
                h3 = tab.find('h3', class_='formtitle')
                full_text = h3.get_text(separator=' ', strip=True)
                
                # Regex mais flexível para achar a chave [ASPLAGMETA-XXXX]
                match_chave = re.search(r'\[([A-Z]+-\d+)\]', full_text)
                if match_chave:
                    reg['Chave'] = match_chave.group(1)
                else:
                    reg['Chave'] = f"SEM-CHAVE-{idx}"

                # O Resumo é o texto do link dentro do h3
                link_resumo = h3.find('a')
                if link_resumo:
                    reg['Resumo'] = link_resumo.get_text(strip=True)
                else:
                    # Se não tem link, limpa a chave do texto completo
                    reg['Resumo'] = full_text.replace(f"[{reg.get('Chave','')}]", "").strip()

                # 2. Identificação do Pai (Meta)
                parent_key = tab.find('a', id='parent_issue_key')
                if parent_key:
                    reg['META_ID'] = parent_key.get_text(strip=True)
                
                parent_summary = tab.find('a', id='parent_issue_summary')
                if parent_summary:
                    reg['Nº_Meta'] = parent_summary.get_text(strip=True)
                else:
                    reg['Nº_Meta'] = ""

                # 3. Dados Internos (Itera sobre linhas)
                # Cuidado: Não entrar em tabelas aninhadas profundas
                cur = tab
                while cur:
                    if cur.name == 'table':
                        # Verifica se é uma tabela de dados (key: value)
                        # Ignora se for cabeçalho de subtarefa (tem muitas células de cabeçalho)
                        rows = cur.find_all('tr')
                        for row in rows:
                            tds = row.find_all(['td', 'th'])
                            # Se tiver muitos th, provavelmente é cabeçalho de lista
                            if len(row.find_all('th')) > 2: continue 

                            for i, td in enumerate(tds):
                                b = td.find('b')
                                if b and (i+1) < len(tds):
                                    key_txt = re.sub(r'\s+', ' ', b.get_text(strip=True).rstrip(':')).strip()
                                    val_txt = tds[i+1].get_text(separator=' ', strip=True)
                                    
                                    # Filtro anti-sujeira
                                    if key_txt and val_txt and val_txt.lower() != 'desconhecido':
                                        reg[key_txt] = val_txt

                    nxt = cur.find_next_sibling()
                    # Para se achar o separador de tickets
                    if not nxt or (nxt.name == 'hr' and 'fullcontent' in nxt.get('class', [])): break
                    cur = nxt
                
                # 4. Fallbacks
                if not reg.get('META_ID'):
                    # Tenta achar em campos genéricos se o link de topo falhou
                    for k_pai in ['Parent', 'Pai', 'Meta Pai']:
                        if k_pai in reg:
                            m = re.search(r'([A-Z]+-\d+)', reg[k_pai])
                            if m:
                                reg['META_ID'] = m.group(1)
                                if not reg['Nº_Meta']:
                                    reg['Nº_Meta'] = reg[k_pai].replace(m.group(1), '').strip(' -:')
                            break
                
                # Se ainda não tem pai, ELE É O PAI -> Nº_Meta = Resumo
                if not reg.get('META_ID') and not reg['Nº_Meta']:
                    reg['Nº_Meta'] = reg.get('Resumo', '')

                reg['Meta_apuração'] = f"[{reg.get('Chave','')}] {reg.get('Resumo','')}"
                
                if reg.get('Chave'): self.dados_extraidos.append(reg)
                
        except Exception as e:
            print(f"❌ Erro HTML: {e}")
        finally:
            self.driver.close()
            self.driver.switch_to.window(self.janela_principal)


    def montar_dicionario_hierarquico(self):
        """Gera estrutura hierárquica Pai → Filhos usando o campo META_ID"""
        print("\n🧱 Montando dicionário hierárquico...")
        
        # Cria um mapa de todos os tickets usando a 'Chave' como índice
        mapa_tickets = {
            registro.get('Chave'): {'Dados': registro, 'Filhos': []}
            for registro in self.dados_extraidos if registro.get('Chave')
        }
        
        dicionario_final = {}
        
        for chave, item in mapa_tickets.items():
            registro = item['Dados']
            chave_pai = registro.get('META_ID')
            
            # Se o ticket tem um pai e esse pai está no nosso mapeamento, adiciona como filho
            if chave_pai and chave_pai in mapa_tickets:
                mapa_tickets[chave_pai]['Filhos'].append(item)
            else:
                # Se não tem pai (ou o pai não foi extraído), é um nó raiz
                dicionario_final[chave] = item
                
        return dicionario_final


    def salvar_json(self, dicionario, nome_arquivo):
        """Salva o dicionário hierárquico em um arquivo JSON na pasta de saída"""
        try:
            caminho = Path(self.config.PASTA_SAIDA) / nome_arquivo
            with open(caminho, 'w', encoding='utf-8') as f:
                json.dump(dicionario, f, indent=4, ensure_ascii=False)
            print(f"💾 JSON salvo com sucesso: {caminho}")
        except Exception as e:
            print(f"❌ Erro ao salvar JSON: {e}")


    def salvar_excel(self, nome_arquivo, gerar_json=False):
        """
        Salva dados extraídos em Excel seguindo a ordem exata do modelo.
        O parâmetro gerar_json resolve o erro de integração com run_anual.
        """
        if not self.dados_extraidos:
            print("\n❌ Nenhum dado para salvar!")
            return
        
        # Converte para DataFrame
        df = pd.DataFrame(self.dados_extraidos)

        # 1. Lista de colunas na ordem exata do seu arquivo modelo
        colunas_modelo = [
            "META_ID", "Chave", "Resumo", "Nº_Meta", "Meta_apuração", 
            "% de Cumprimento", "Afeta as versões", "Ano da Meta", 
            "Cargo do Gerente Responsável", "Cloners", "Componentes", "Criador", 
            "Data da Aprovação pelo Comitê de Governança e Gestão Estratégica", 
            "Data da Entrega do Formulário", "Data de Apuração", "Dirigência Responsável", 
            "E-mail do Gerente Responsável", "E-mail do Responsável pelo Preenchimento", 
            "Estado", "Etiquetas", "Fim Efetivo", "Fim Previsto", "Fonte da Informação", 
            "Forma de apuração do resultado final", "Fórmula de Cálculo", 
            "Gerente Responsável", "Indicador Estratégico", "Informação complementar", 
            "Iniciativas Estratégicas 2025", "Início Efetivo", "Início Previsto", 
            "Links de ocorrências", "Macrodesafio", "Meta e Indicador", 
            "Nome do Responsável pelo Preenchimento", "Objetivo de Desenvolvimento Sustentável (ODS)", 
            "Outras Unidades Envolvidas", "Patrocinador", "Periodicidade", 
            "Planos Institucionais", "Polaridade", "Prioridade", "Projeto", 
            "Resolução", "Responsável", "Subtarefas", "Telefone do Gerente Responsável", 
            "Tipo", "Tipo de Meta", "Unidade Gestora", "Unidade de Medida", 
            "Valor Apurado", "Valor da Meta", "Versões de correção", "Votos"
        ]

        # 2. Reorganização: mantém a ordem do modelo para o que existir, 
        # e adiciona campos novos ao final (caso o Jira mude)
        existentes_no_modelo = [c for c in colunas_modelo if c in df.columns]
        novas_colunas = [c for c in df.columns if c not in colunas_modelo]
        
        df = df[existentes_no_modelo + novas_colunas]

        # 3. Salva o Excel
        caminho = Path(self.config.PASTA_SAIDA) / nome_arquivo
        df.to_excel(caminho, index=False)
        print(f"\n💾 Excel formatado salvo: {caminho}")

        # 4. Processa o JSON se solicitado (resolve o erro da linha 447)
        if gerar_json:
            dicionario = self.montar_dicionario_hierarquico()
            # Tenta usar o nome do arquivo excel trocando a extensão para .json
            nome_json = nome_arquivo.replace('.xlsx', '.json')
            self.salvar_json(dicionario, nome_json)


    # ============================================
    # MÉTODOS DE EXECUÇÃO
    # ============================================

    def run_simples(self):
        print("\n🚀 MODO: SIMPLES")
        self.criar_pasta_saida()
        self.iniciar_navegador()
        self.login_manual_e_aguardar()
        self.navegar_jql(f"{self.config.JQL_CORE} ORDER BY created DESC")
        if self.exportar_detalhes_impressao():
            self.processar_aba_exportacao()
            self.salvar_excel(self.config.ARQUIVO_JIRA_SIMPLES)
        self.fechar()

    def run_anual(self):
        print("\n🚀 MODO: ANUAL")
        self.criar_pasta_saida()
        self.iniciar_navegador()
        self.login_manual_e_aguardar()
        for ano in self.config.ANOS_EXTRACAO:
            print(f"📅 {ano}")
            self.navegar_jql(f'{self.config.JQL_CORE} AND "Ano da Meta" = {ano} ORDER BY created DESC')
            if self.exportar_detalhes_impressao():
                self.processar_aba_exportacao()
        self.salvar_excel(self.config.ARQUIVO_JIRA_ANUAL, gerar_json=True)
        self.fechar()

    def run_completo(self):
        print("\n🚀 MODO: COMPLETO")
        self.criar_pasta_saida()
        self.iniciar_navegador()
        self.login_manual_e_aguardar()
        
        print("--- Etapa 1: Simples ---")
        self.navegar_jql(f"{self.config.JQL_CORE} ORDER BY created DESC")
        if self.exportar_detalhes_impressao():
            self.processar_aba_exportacao()
            self.salvar_excel(self.config.ARQUIVO_JIRA_SIMPLES)
        self.dados_extraidos = [] 
        
        print("--- Etapa 2: Anual ---")
        for ano in self.config.ANOS_EXTRACAO:
            print(f"📅 {ano}")
            self.navegar_jql(f'{self.config.JQL_CORE} AND "Ano da Meta" = {ano} ORDER BY created DESC')
            if self.exportar_detalhes_impressao():
                self.processar_aba_exportacao()
        self.salvar_excel(self.config.ARQUIVO_JIRA_ANUAL, gerar_json=True)
        self.fechar()
        
        self.processador.processar_estilo_notebook()


if __name__ == "__main__":
    print("🎯 EXTRATOR JIRA v3.10")
    print("1. Simples | 2. Anual | 3. Completo | 4. Offline")
    opt = input("Opção: ").strip()
    config = Config()
    if opt == '4': ProcessadorJira(config).processar_estilo_notebook()
    else:
        ext = ExtratorJira(config)
        if opt == '1': ext.run_simples()
        elif opt == '2': ext.run_anual()
        elif opt == '3': ext.run_completo()
        else: print("Opção inválida")