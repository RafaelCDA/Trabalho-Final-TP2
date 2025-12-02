"""
SERVIÇO DE ESTATÍSTICAS - Para relatórios do professor
"""
import json
import os
from datetime import datetime
from typing import Dict, List

class EstatisticasService:
    def __init__(self):
        self.arquivo_dados = "dados/estatisticas_pesquisas.json"
        os.makedirs("dados", exist_ok=True)
    
    def registrar_busca(self, termo: str, usuario_lat: float, usuario_long: float, 
                       resultados_count: int):
        """Registra estatística de busca para relatórios"""
        estatistica = {
            "termo": termo,
            "data_hora": datetime.now().isoformat(),
            "localizacao_usuario": {"lat": usuario_lat, "long": usuario_long},
            "resultados_encontrados": resultados_count
        }
        
        # Salva em arquivo JSON (simples)
        dados = self._carregar_dados()
        dados["pesquisas"].append(estatistica)
        self._salvar_dados(dados)
    
    def obter_relatorio_pesquisas(self) -> Dict:
        """Gera relatório para administrador"""
        dados = self._carregar_dados()
        
        # Estatísticas básicas para relatório
        return {
            "total_pesquisas": len(dados["pesquisas"]),
            "termos_mais_buscados": self._calcular_termos_populares(dados),
            "pesquisas_sem_resultados": self._calcular_pesquisas_sem_resultado(dados),
            "ultimas_pesquisas": dados["pesquisas"][-10:]  # Últimas 10
        }
    
    def _calcular_termos_populares(self, dados: Dict) -> List[Dict]:
        """Calcula termos mais buscados"""
        termos = {}
        for pesquisa in dados["pesquisas"]:
            termo = pesquisa["termo"]
            termos[termo] = termos.get(termo, 0) + 1
        
        return [{"termo": k, "quantidade": v} for k, v in termos.items()]
    
    def _calcular_pesquisas_sem_resultado(self, dados: Dict) -> int:
        """Conta pesquisas que não encontraram resultados"""
        return sum(1 for p in dados["pesquisas"] if p["resultados_encontrados"] == 0)
    
    def _carregar_dados(self) -> Dict:
        """Carrega dados do arquivo"""
        try:
            with open(self.arquivo_dados, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"pesquisas": []}
    
    def _salvar_dados(self, dados: Dict):
        """Salva dados no arquivo"""
        with open(self.arquivo_dados, 'w') as f:
            json.dump(dados, f, indent=2)
