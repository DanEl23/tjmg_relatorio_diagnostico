import pandas as pd
import numpy as np
import sys
from pathlib import Path

class CNJDataLoader:
    def __init__(self, csv_filename='JN_15-Jan-2026.csv'):
        # --- LÓGICA DE CAMINHOS ROBUSTA ---
        # 1. Pega o diretório onde ESTE arquivo (cnj_loader.py) está: .../src/extractors
        current_dir = Path(__file__).resolve().parent
        
        # 2. Navega até a raiz do projeto (sobe 2 níveis: extractors -> src -> raiz)
        project_root = current_dir.parent.parent
        
        # 3. Monta o caminho absoluto até o CSV em data/raw
        self.csv_path = project_root / 'data' / 'raw' / csv_filename
        
        self.df = None
        self.ano_base = None

    def _limpar_numero(self, val):
        """Converte strings numéricas BR (1.000,00) para float."""
        if isinstance(val, str):
            val = val.replace('.', '').replace(',', '.')
            try:
                return float(val)
            except ValueError:
                return np.nan
        return val

    def _formatar_br(self, val, decimais=0):
        """Formata float para string BR."""
        if pd.isna(val) or val == 0: return "s/d"
        return f"{val:,.{decimais}f}".replace(',', 'X').replace('.', ',').replace('X', '.')

    def _formatar_pct(self, val):
        """Formata percentual."""
        if pd.isna(val): return "s/d"
        # Ajuste inteligente de escala (se vier 0.7 ou 70.0)
        multiplicador = 100 if val <= 1 else 1 
        return f"{val * multiplicador:,.1f}%".replace('.', ',')

    def carregar_dados(self):
        print(f"   [DEBUG] Procurando arquivo em: {self.csv_path}")
        
        if not self.csv_path.exists():
            raise FileNotFoundError(f"Arquivo CSV não encontrado no caminho esperado: {self.csv_path}")

        # Carrega o CSV
        self.df = pd.read_csv(self.csv_path, sep=';', encoding='latin1', on_bad_lines='skip', low_memory=False)
        
        # Lista de colunas numéricas críticas para limpar
        cols_numericas = ['dpj', 'cn', 'cp', 'ch', 'mag', 'serv', 'dmag', 'dserv', 'ftt', 'ipm', 'ipsjud', 'tc', 'tcl', 'eff', 'munic', 'tbaix']
        
        for col in cols_numericas:
            if col in self.df.columns:
                self.df[col] = self.df[col].apply(self._limpar_numero)

    def get_dados_tribunal(self, sigla='TJMG'):
        if self.df is None:
            self.carregar_dados()

        # Filtrar Tribunal e Ano Mais Recente
        df_trib = self.df[self.df['sigla'] == sigla]
        if df_trib.empty:
            print(f"   [AVISO] Tribunal {sigla} não encontrado no CSV.")
            return {}
            
        self.ano_base = df_trib['ano'].max()
        row = df_trib[df_trib['ano'] == self.ano_base].iloc[0]

        # Cálculos Auxiliares
        cn = row.get('cn', 0)
        ch = row.get('ch', 0)
        populacao = (cn / ch * 100000) if ch > 0 else 0
        
        # Ranking Porte
        ranking_texto = "s/d"
        try:
            porte = row['idporte']
            df_ano = self.df[(self.df['ano'] == self.ano_base) & (self.df['justica'] == 'Estadual') & (self.df['idporte'] == porte)]
            rank = df_ano['dpj'].rank(ascending=False)
            posicao = int(rank[self.df['sigla'] == sigla].iloc[0])
            ranking_texto = f"{posicao}º lugar"
        except:
            pass

        # Montar Dicionário Final (Mapeamento)
        return {
            "Ano base": str(self.ano_base),
            "Ano de edição do relatório": str(self.ano_base + 1),
            "Nº de municípios-sede": self._formatar_br(row.get('munic')),
            "Classificação do TJMG dentro do Grupo ‘Grande Porte’": ranking_texto,
            "Nº de magistrados": self._formatar_br(row.get('mag')),
            "Força de trabalho (servidores e auxiliares) (*)": self._formatar_br(row.get('ftt')),
            "Despesa total da justiça (Bilhões)": self._formatar_br(row.get('dpj'), 0),
            "Despesa total por habitante, incluindo custo com inativos (Reais)": self._formatar_br(row.get('dpj') / populacao, 1) if populacao else "s/d",
            "Custo médio mensal com magistrados (Milhões)": self._formatar_br((row.get('dmag') / row.get('mag') / 12), 0) if row.get('mag') else "s/d",
            "Custo médio mensal com servidores (Milhões)": self._formatar_br((row.get('dserv') / row.get('serv') / 12), 0) if row.get('serv') else "s/d",
            "Casos novos": self._formatar_br(row.get('cn')),
            "Casos pendentes": self._formatar_br(row.get('cp')),
            "Casos novos por 100 mil habitantes": self._formatar_br(row.get('ch')),
            "Índice de produtividade dos magistrados": self._formatar_br(row.get('ipm')),
            "Índice de produtividade de servidores da área judiciária": self._formatar_br(row.get('ipsjud')),
            "Índice de atendimento à demanda (Geral)": self._formatar_pct(row.get('tbaix') / row.get('cn')) if row.get('cn') else "s/d",
            "Taxa de congestionamento Total": self._formatar_pct(row.get('tc')),
            "Taxa de congestionamento líquida": self._formatar_pct(row.get('tcl')),
            "Resultado do IPC-Jus total por tribunal (incluída a área administrativa)": self._formatar_pct(row.get('eff')),
            # Métricas DEA/Complexas
            "Índice de produtividade dos magistrados (IPM) realizado x necessário para que tribunal atinja IPC-Jus de 100%.": f"{self._formatar_br(row.get('ipm'))}, s/d",
            "Taxa de congestionamento líquida (TCL) realizado x resultado da consequência se tribunal atingisse IPC-Jus 100%. TCL realizado": f"{self._formatar_pct(row.get('tcl'))}, s/d"
        }