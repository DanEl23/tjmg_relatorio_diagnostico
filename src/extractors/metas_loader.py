"""
Módulo para carregar e processar dados de metas do arquivo metas_institucionais_2025.xlsx

Estrutura esperada:
- Aba "Valores Apurados": Meta, 2022, 2023, 2024, 2025 (valores apurados)
- Aba "Textos Metas": Meta, Nº_Meta, Ano da Meta, Valor da Meta (descrição)
"""

import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class MetasInstitucionaisLoader:
    """Carregador de dados de metas institucionais do arquivo Excel."""
    
    def __init__(self, caminho_arquivo: str = None):
        """
        Inicializa o carregador.
        
        Args:
            caminho_arquivo: Caminho para metas_institucionais_2025.xlsx.
                            Se None, busca em exports/
        """
        if caminho_arquivo is None:
            # Busca automaticamente o arquivo
            base_dir = Path(__file__).parent.parent.parent
            caminho_arquivo = base_dir / "exports" / "metas_institucionais_2025.xlsx"
        
        self.caminho = Path(caminho_arquivo)
        
        if not self.caminho.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {self.caminho}")
        
        # Carrega as abas
        self.df_valores = pd.read_excel(self.caminho, sheet_name='Valores Apurados')
        self.df_textos = pd.read_excel(self.caminho, sheet_name='Textos Metas')
    
    def obter_meta(self, nome_meta: str) -> Optional[Dict]:
        """
        Obtém dados de uma meta específica.
        
        Args:
            nome_meta: Nome da meta (ex: "TJMG 5")
        
        Returns:
            Dict com dados da meta ou None se não encontrada
        """
        # Busca na aba de valores
        valores = self.df_valores[self.df_valores['Meta'] == nome_meta]
        
        if valores.empty:
            return None
        
        # Busca na aba de textos
        textos = self.df_textos[self.df_textos['Meta'] == nome_meta]
        
        meta_data = {
            'nome': nome_meta,
            'valor_meta': None,
            'anos': [],
            'valores': [],
            'textos': {}
        }
        
        # Extrai valor da meta
        if not textos.empty:
            meta_data['valor_meta'] = textos.iloc[0]['Valor da Meta']
            meta_data['textos'] = textos.iloc[0].to_dict()
        
        # Extrai valores por ano (2022, 2023, 2024, 2025)
        if not valores.empty:
            row = valores.iloc[0]
            for ano in [2022, 2023, 2024, 2025]:
                if ano in row.index:
                    meta_data['anos'].append(ano)
                    meta_data['valores'].append(row[ano])
        
        return meta_data
    
    def obter_todas_metas(self) -> List[str]:
        """Retorna lista de todas as metas disponíveis."""
        return sorted(self.df_valores['Meta'].unique().tolist())
    
    def obter_dados_tabela_meta_por_ano(
        self, 
        nome_meta: str
    ) -> Optional[Tuple[List[str], List[str], List[str]]]:
        """
        Retorna dados formatados para tabela de meta única com colunas por ano.
        
        Args:
            nome_meta: Nome da meta (ex: "TJMG 5")
        
        Returns:
            Tuple com (anos, valores_meta, valores_resultado) ou None
            Exemplo:
                (['2022', '2023', '2024', '2025'], ['—', '70%', '70%', '70%'], ['—', '60%', '65%', '64%'])
        """
        meta_data = self.obter_meta(nome_meta)
        
        if meta_data is None:
            return None
        
        anos = meta_data['anos']
        valores = meta_data['valores']
        valor_meta = meta_data['valor_meta']
        
        # Formata anos como strings
        anos_str = [str(int(ano)) for ano in anos]
        
        # Formata valor da meta (primeira linha)
        # Se valor_meta existe e é numérico, formata como %
        valores_meta_str = []
        if valor_meta is not None and not pd.isna(valor_meta):
            # Primeira coluna (2022) geralmente não tem valor
            valores_meta_str.append('—')
            # Outros anos têm o valor da meta
            for ano in anos[1:]:
                if not pd.isna(valor_meta):
                    valores_meta_str.append(f"{valor_meta:.0f}%")
                else:
                    valores_meta_str.append('—')
        else:
            valores_meta_str = ['—'] * len(anos)
        
        # Formata resultados (segunda linha)
        valores_resultado = []
        for val in valores:
            if pd.isna(val):
                valores_resultado.append('—')
            elif val == int(val):
                valores_resultado.append(f"{int(val)}%")
            else:
                valores_resultado.append(f"{val:.1f}%")
        
        return anos_str, valores_meta_str, valores_resultado
    
    def formatar_valor(self, valor, eh_percentual: bool = True) -> str:
        """
        Formata um valor para exibição.
        
        Args:
            valor: Valor a formatar
            eh_percentual: Se deve adicionar %
        
        Returns:
            Valor formatado como string
        """
        if pd.isna(valor):
            return '—'
        
        try:
            if eh_percentual:
                if float(valor) == int(float(valor)):
                    return f"{int(float(valor))}%"
                else:
                    return f"{float(valor):.1f}%"
            else:
                if float(valor) == int(float(valor)):
                    return str(int(float(valor)))
                else:
                    return f"{float(valor):.2f}"
        except (ValueError, TypeError):
            return '—'


# Exemplo de uso
if __name__ == "__main__":
    loader = MetasInstitucionaisLoader()
    
    print("=" * 80)
    print("TESTE: MetasInstitucionaisLoader")
    print("=" * 80)
    
    # Lista todas as metas
    metas = loader.obter_todas_metas()
    print(f"\n✓ Metas disponíveis ({len(metas)} total):")
    for meta in metas[:10]:
        print(f"  - {meta}")
    
    # Obtém dados de uma meta específica
    print("\n" + "=" * 80)
    meta_teste = "TJMG 5"
    print(f"✓ Dados da meta: {meta_teste}")
    data = loader.obter_meta(meta_teste)
    if data:
        print(f"  Nome: {data['nome']}")
        print(f"  Valor da Meta: {data['valor_meta']}")
        print(f"  Anos: {data['anos']}")
        print(f"  Valores: {data['valores']}")
    
    # Obtém dados formatados para tabela
    print("\n" + "=" * 80)
    print(f"✓ Dados para tabela de meta por ano:")
    resultado = loader.obter_dados_tabela_meta_por_ano(meta_teste)
    if resultado:
        anos, valores_meta, valores_resultado = resultado
        print(f"  Anos:     {anos}")
        print(f"  Meta:     {valores_meta}")
        print(f"  Resultado: {valores_resultado}")
