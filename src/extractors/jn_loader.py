import pandas as pd
from pathlib import Path

class CarregadorJN:
    def __init__(self, caminho_csv_dados, caminho_csv_vars=None):
        self.caminho_dados = Path(caminho_csv_dados)
        self.caminho_vars = Path(caminho_csv_vars) if caminho_csv_vars else None
        self.df = None
        self.df_vars = None
        self.anos_disponiveis = []
        self.mapa_vars = {}

    def carregar(self):
        """ Lê os CSVs tratando separadores e encoding """
        if not self.caminho_dados.exists():
            print(f"❌ Erro: Arquivo não encontrado: {self.caminho_dados}")
            return

        print(f"🔄 Carregando base Justiça em Números: {self.caminho_dados.name}...")
        
        # Leitura dos Dados
        try:
            self.df = pd.read_csv(self.caminho_dados, sep=';', encoding='latin1', low_memory=False)
        except:
            self.df = pd.read_csv(self.caminho_dados, sep=';', encoding='utf-8', low_memory=False)

        # --- CORREÇÃO 1: Normaliza colunas para minúsculo e remove espaços ---
        # Isso garante que 'IPCM', 'Ipcm' e 'ipcm ' virem 'ipcm'
        self.df.columns = self.df.columns.str.strip().str.lower()

        # Leitura do Dicionário de Variáveis
        if self.caminho_vars and self.caminho_vars.exists():
            try:
                self.df_vars = pd.read_csv(self.caminho_vars, sep=';', encoding='latin1')
            except:
                self.df_vars = pd.read_csv(self.caminho_vars, sep=';', encoding='utf-8')
            
            # Normaliza também as colunas do dicionário
            self.df_vars.columns = self.df_vars.columns.str.strip().str.lower()

            if 'sigla' in self.df_vars.columns and 'dsc_sigla' in self.df_vars.columns:
                # Normaliza as chaves do dicionário para minúsculo também
                self.df_vars['sigla'] = self.df_vars['sigla'].str.strip().str.lower()
                self.mapa_vars = dict(zip(self.df_vars['sigla'], self.df_vars['dsc_sigla']))
        
        # Limpeza básica e identificação de anos
        if 'ano' in self.df.columns:
            self.df['ano'] = pd.to_numeric(self.df['ano'], errors='coerce')
            self.anos_disponiveis = sorted(self.df['ano'].dropna().unique().astype(int))
            print(f"✅ Dados carregados! Anos disponíveis: {self.anos_disponiveis}")
        else:
            print("❌ Erro: Coluna 'ano' não encontrada no CSV.")

    def _formatar_valor(self, valor):
        """ Formata float/string para padrão BR (1.234,5) """
        if pd.isna(valor) or str(valor).strip().lower() in ['nd', '', 'nan', 'inf', '-inf']:
            return "-"
        
        try:
            if isinstance(valor, str):
                valor = float(valor.replace('.', '').replace(',', '.'))
            
            if valor.is_integer():
                return "{:,.0f}".format(valor).replace(',', '.')
            
            return "{:,.1f}".format(valor).replace(',', '.')
        except:
            return str(valor)

    def obter_tabela_serie_historica(self, tribunal_sigla, lista_variaveis, anos=None, titulo_grupo="Indicadores"):
        """
        Gera a matriz de dados para o builders.adicionar_tabela_justica_numeros
        """
        if self.df is None: self.carregar()

        if not anos:
            anos = self.anos_disponiveis[-6:]

        # Normaliza filtro de tribunal
        if 'sigla' in self.df.columns:
            df_trib = self.df[self.df['sigla'].str.upper() == tribunal_sigla.upper()].copy()
        else:
            print("❌ Erro: Coluna 'sigla' não encontrada.")
            return []

        dados_saida = []
        
        # 1. Título do Grupo
        dados_saida.append(['HEADER_MERGE', titulo_grupo] + [''] * 6)

        # 2. Cabeçalho dos Anos
        header_anos = ['SUB_HEADER', 'Indicador'] + [str(a) for a in anos]
        while len(header_anos) < 8: header_anos.append("")
        dados_saida.append(header_anos[:8])

        # 3. Linhas de Dados
        for var_cod in lista_variaveis:
            # Garante que estamos buscando em minúsculo
            var_cod_lower = var_cod.lower().strip()
            
            # --- CORREÇÃO 2: Verificação de Existência da Coluna ---
            if var_cod_lower not in self.df.columns:
                print(f"⚠️ Aviso: Variável '{var_cod}' não encontrada no CSV. Preenchendo com 'N/D'.")
                # Adiciona linha vazia/erro mas não quebra o código
                linha = ['DATA_ROW', f"{var_cod} (Não encontrado)"] + ["N/D"] * len(anos)
            else:
                nome_indicador = self.mapa_vars.get(var_cod_lower, var_cod)
                if len(nome_indicador) > 60:
                    nome_indicador = nome_indicador[:57] + "..."

                linha = ['DATA_ROW', nome_indicador]

                for ano in anos:
                    val = df_trib[df_trib['ano'] == ano][var_cod_lower]
                    val_fmt = self._formatar_valor(val.values[0]) if not val.empty else "-"
                    linha.append(val_fmt)
            
            # Ajusta para 7 colunas (limite da tabela)
            while len(linha) < 8: linha.append("")
            dados_saida.append(linha[:8])

        return dados_saida