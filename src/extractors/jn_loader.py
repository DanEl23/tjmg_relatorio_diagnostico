import pandas as pd
import numpy as np
from pathlib import Path

class CarregadorJN:
    def __init__(self, caminho_csv_dados, caminho_csv_manual):
        self.caminho_dados = Path(caminho_csv_dados)
        self.caminho_manual = Path(caminho_csv_manual)
        self.df = None
        self.df_manual = None
        
        # =================================================================
        # MAPA DE MÉTRICAS ATUALIZADO (SUA VERSÃO)
        # =================================================================
        self.mapa_metricas = {
            # --- ESTRUTURA ---
            "municipios": "comarca",
            "pop_sede_perc": "pop_sede_perc", # Manual (Direto)
            "unidades_jud": "varaje",
            "ranking_tjmg": "ranking_manual", # Manual (Direto)
            "magistrados": "mag",
            "forca_trabalho": ["ts", "tfaux"], # ATENÇÃO: Mudou de tf para ts
            "despesa_total": "dpj",
            "despesa_hab": "g7",
            "custo_magistrado": "custo_magistrado", # Agora busca coluna direta
            "custo_servidor": "custo_servidor",     # Agora busca coluna direta
            "perc_cargos_vagos_mag": ("magv", "mag"), 
            "perc_serv_adm": "servadmseti",
            
            # --- MOVIMENTAÇÃO ---
            "casos_novos": "cn",
            "casos_pendentes": "cp",
            "cn_100k_hab": "ch",
            "ipm": "ipm",
            "ips": "ips",
            "perc_serv_jud_1grau": "serv1_perc", # Manual (Direto)
            "iad": "iad",
            
            # --- DIGITAL ---
            "perc_eletr": ("cnelet", "cn"), 
            "perc_unidades_j100": "j100_perc", # Manual (Direto)
            "nucleos_40": "n4", # Manual (Direto)
            "balcao_virtual": "bv", # Manual (Direto)
            
            # --- DETALHAMENTO ---
            "cn_mag_1": ("cn1", "mag1"),
            "cn_mag_2": ("cn2", "mag2"),
            "cn_serv_1": "cs1",
            "cn_serv_2": "cs2",
            "carga_mag_1": "k1",
            "carga_mag_2": "k2",
            "carga_serv_1": "ks1",
            "carga_serv_2": "ks2",
            "ipm_1": "ipm1",
            "ipm_2": "ipm2",
            "ips_1": "ipsjud1",
            "ips_2": "ipsjud2",
            "iad_1": "iad1",
            "iad_2": "iad2",
            "ind_cn_eletr": ("cnelet", "cn"),
            "perc_eletr_1": ("cnelet1", "cn1"),
            "perc_eletr_2": ("cnelet2", "cn2"),
            
            # --- TAXAS ---
            "tc_total": "tc",
            "tc_liq": "tcl",
            "tc_1": "tc1",
            "tc_2": "tc2",
            "tc_conhec": "tcc1",
            "tc_exec": "tcex1",
            "tc_exec_fiscal": "tcextfisc1",
            
            # --- RECORRIBILIDADE ---
            "rin_geral": "rin",
            "rx_geral": "rx",
            "rin_1": "rin1",
            "rin_2": "rin2",
            "rx_1": "rx1",
            "rx_2": "rx2",
            
            # --- OUTROS ---
            "perc_pend_exec_estoque": ("cpextfisc1", "cp"),
            "pend_exec_fiscal": "cpextfisc1",
            "cejusc": "cejusc",
            "ic_geral": "ic",
            "ic_1": "ic1",
            "ic_2": "ic2",
            "tempo_sent_1": "tempo_sent_1", # Agora busca coluna direta
            "tempo_sent_2": "tempo_sent_2", # Agora busca coluna direta
            "tempo_giro": "t_giro",     # Manual
            "tempo_fisico": "tm_fis",   # Manual
            "tempo_eletr": "tm_elet",   # Manual
            "cn_crim": "cncrim",
            "cp_crim": "cpcrim",
            "ipc_jus": "eff",
            "ipc_jus_1": "eff1",
            "ipc_jus_2": "eff2",
            "ipm_meta": ["ipm", "ipmtarget"],
            "ips_meta": ["ips", "ipstarget"],
            "tcl_meta": ["tcl", "tcltarget"]
        }

    def carregar(self):
        """ Versão Ultra-Resiliente: Detecta separadores e encodings automaticamente """
        # 1. Carregando dados do CNJ
        if self.caminho_dados.exists():
            try:
                self.df = pd.read_csv(
                    self.caminho_dados, sep=None, engine='python', encoding='latin1', on_bad_lines='skip'
                )
                self.df.columns = self.df.columns.str.strip().str.lower()
                
                cols_num = self.df.columns.drop(['justica', 'sigla', 'uf'], errors='ignore')
                for col in cols_num:
                    if self.df[col].dtype == object:
                        self.df[col] = self.df[col].astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
                        self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
                
                if 'ano' in self.df.columns:
                    self.df['ano'] = pd.to_numeric(self.df['ano'], errors='coerce').fillna(0).astype(int)
                    
            except Exception as e: print(f"❌ Erro ao carregar CNJ: {e}")

        # 2. Carregando dados MANUAIS
        if self.caminho_manual.exists():
            try:
                self.df_manual = pd.read_csv(
                    self.caminho_manual, sep=None, engine='python', encoding='latin1', on_bad_lines='skip'
                )
                self.df_manual.columns = [str(c).strip().lower() for c in self.df_manual.columns]
                
                if 'ano' not in self.df_manual.columns:
                    self.df_manual = self.df_manual.reset_index()
                    self.df_manual.columns = [str(c).strip().lower() for c in self.df_manual.columns]
                
                if 'ano' in self.df_manual.columns:
                    self.df_manual['ano'] = pd.to_numeric(self.df_manual['ano'], errors='coerce').fillna(0).astype(int)
                    print(f"✅ Dados manuais carregados. Colunas: {list(self.df_manual.columns)}")
                else:
                    print(f"⚠️ Alerta: Coluna 'ano' não encontrada no manual.")
            except Exception as e: print(f"❌ Erro ao carregar Manual: {e}")

    def _obter_valor(self, df_ano, coluna):
        ano_alvo = df_ano.iloc[0]['ano']
        # 1. Busca no Manual
        if self.df_manual is not None:
            row_m = self.df_manual[self.df_manual['ano'] == ano_alvo]
            if not row_m.empty and coluna in row_m.columns:
                val = row_m.iloc[0][coluna]
                if pd.notna(val): return val
        # 2. Busca no CNJ
        if coluna in df_ano.columns:
            val = df_ano.iloc[0][coluna]
            return val if pd.notna(val) else 0
        return 0

    def _formatar(self, valor, is_percent=False):
        """ Formata para padrão BR (1.000,00) """
        if pd.isna(valor) or valor == np.inf or valor == -np.inf: return "-"
        if valor == 0: return "-"
        
        try:
            val_float = float(valor)
            
            # Caso 1: Porcentagem (Sempre 1 casa decimal)
            if is_percent:
                texto = "{:,.1f}".format(val_float) 
                texto = texto.replace(',', 'X').replace('.', ',').replace('X', '.')
                return texto + "%"

            # Caso 2: Inteiro puro
            if val_float.is_integer():
                texto = "{:,.0f}".format(val_float)
                return texto.replace(',', '.')

            # Caso 3: Decimal (1 casa)
            else:
                texto = "{:,.1f}".format(val_float)
                texto = texto.replace(',', 'X').replace('.', ',').replace('X', '.')
                return texto

        except: return str(valor)

    def _calcular_composto(self, df_ano, chave):
        regra = self.mapa_metricas.get(chave, chave)
        
        # 1. Soma (Força Trabalho: TS + TFAUX)
        if chave == "forca_trabalho" and isinstance(regra, list):
            v1 = self._obter_valor(df_ano, regra[0])
            v2 = self._obter_valor(df_ano, regra[1])
            return self._formatar(v1 + v2)

        # 2. Tupla (Divisão -> % ou Média)
        if isinstance(regra, tuple):
            v_num = self._obter_valor(df_ano, regra[0])
            v_den = self._obter_valor(df_ano, regra[1])
            if v_den == 0: return "-"
            
            # Métricas que são MÉDIA (divisão simples) e não porcentagem
            metricas_media = ['cn_mag_1', 'cn_mag_2']
            
            if chave in metricas_media:
                return self._formatar(v_num / v_den, is_percent=False)
            else:
                return self._formatar((v_num / v_den) * 100, is_percent=True)

        # 3. Lista (Concatenação)
        elif isinstance(regra, list):
            vals = []
            for col in regra:
                val = self._obter_valor(df_ano, col)
                # Multiplica decimais se necessário
                if col in ['tcl', 'tcltarget', 'ipm', 'ipmtarget', 'ips', 'ipstarget', 'iad']:
                    if col in ['tcl', 'tcltarget', 'iad'] and val is not None and val <= 1.5:
                         val = val * 100
                vals.append(self._formatar(val))
            return " / ".join(vals)

        # 4. Valor Direto
        else:
            val = self._obter_valor(df_ano, regra)
            
            # Multiplica se for decimal pequeno (0.77 -> 77)
            colunas_decimais = [
                'iad', 'iad1', 'iad2', 'tc', 'tcl', 'tc1', 'tc2',
                'tcc1', 'tcex1', 'tcextfisc1', 'rin', 'rx', 'rin1', 'rin2', 
                'rx1', 'rx2', 'ic', 'ic1', 'ic2', 'eff', 'eff1', 'eff2'
            ]
            if regra in colunas_decimais and val is not None and val <= 1.5 and val > 0:
                val = val * 100
            
            # Adiciona %
            colunas_pct = ['pop_sede_perc', 'serv1_perc', 'j100_perc', 'perc_serv_adm'] + colunas_decimais
            is_pct = regra in colunas_pct or "perc" in regra
            
            return self._formatar(val, is_percent=is_pct)

    def obter_dados_tabela(self, tribunal_sigla, lista_metricas_amigaveis, anos, titulos_linhas=None):
        if self.df is None: self.carregar()
        if self.df is None: return []
        
        df_trib = self.df[self.df['sigla'].str.upper() == tribunal_sigla.upper()].copy()
        dados_saida = []
        
        header = ['SUB_HEADER', 'Indicador'] + [str(a) for a in anos]
        dados_saida.append(header + [""] * (8 - len(header)))

        for i, chave in enumerate(lista_metricas_amigaveis):
            label = titulos_linhas[i] if titulos_linhas and i < len(titulos_linhas) else chave
            linha = ['DATA_ROW', label]
            for ano in anos:
                df_ano = df_trib[df_trib['ano'] == ano]
                linha.append(self._calcular_composto(df_ano, chave) if not df_ano.empty else "-")
            dados_saida.append(linha + [""] * (8 - len(linha)))
            
        return dados_saida