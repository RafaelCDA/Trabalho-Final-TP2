"""
Serviço responsável pelas operações de busca (pesquisas).

Permite:
- registrar a pesquisa
- buscar produtos e bancas pelo termo
- filtrar por preço máximo
- filtrar por distância máxima
- ordenar por distância ou preço
- combinar filtros
"""

import math
from typing import Optional, List

from sqlalchemy.orm import Session

from src.dto.pesquisa_dto import SearchResponse
from src.dto.produto_dto import ProdutoRead
from src.dto.banca_dto import BancaRead

from src.repositories.pesquisa_repository import PesquisaRepository
from src.repositories.produto_repository import ProdutoRepository
from src.repositories.banca_repository import BancaRepository


# ============================================================
# FUNÇÃO DE DISTÂNCIA (HAVERSINE)
# ============================================================


def calcular_distancia(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calcula a distância entre dois pontos GPS usando a fórmula de Haversine.
    Retorna distância em quilômetros.
    """
    R = 6371  # raio da Terra (km)

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )

    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


# ============================================================
# SERVIÇO DE PESQUISA
# ============================================================


class PesquisaService:
    def __init__(self, db: Session):
        self.db = db
        self.produto_repo = ProdutoRepository(db)
        self.banca_repo = BancaRepository(db)
        self.pesquisa_repo = PesquisaRepository(db)

    # --------------------------------------------------------
    # Buscar produtos e/ou bancas com filtros avançados
    # --------------------------------------------------------
    def buscar(
        self,
        termo: str,
        tipo: str,
        lat_user: Optional[float],
        lon_user: Optional[float],
        preco_max: Optional[float] = None,
        distancia_max_metros: Optional[float] = None,
        order_by: Optional[str] = None,
        lat_ref: Optional[float] = None,
        lon_ref: Optional[float] = None,
    ) -> SearchResponse:
        """
        Executa busca com filtros de preço e distância.
        lat_ref/lon_ref: localização opcional para filtrar por proximidade.
        lat_user/lon_user: localização real do usuário (para registrar).
        """

        # --------------------------------------------------------
        # 1. Registrar a pesquisa
        # --------------------------------------------------------
        self.pesquisa_repo.registrar(
            termo=termo,
            latitude=lat_user,
            longitude=lon_user,
        )

        produtos_result: List[ProdutoRead] = []
        bancas_result: List[BancaRead] = []

        # Se o filtro de distância foi informado, convertemos de METROS → KM
        distancia_max_km = None
        if distancia_max_metros is not None:
            distancia_max_km = distancia_max_metros / 1000.0

        # Localização a ser usada para filtros/ordenar
        lat_filtro = lat_ref if lat_ref is not None else lat_user
        lon_filtro = lon_ref if lon_ref is not None else lon_user

        # --------------------------------------------------------
        # 2. Buscar PRODUTOS
        # --------------------------------------------------------
        if tipo in ("produto", "all"):
            produtos = self.produto_repo.get_all()

            # etapa 1: filtrar pelo nome
            produtos = [p for p in produtos if termo.lower() in p.nome.lower()]

            # etapa 2: aplicar filtro de preço
            if preco_max is not None:
                produtos = [p for p in produtos if p.preco <= preco_max]

            # etapa 3: filtrar por distância
            if distancia_max_km is not None and lat_filtro and lon_filtro:
                filtrados = []
                for p in produtos:
                    addr = p.banca.address
                    if addr.latitude is None or addr.longitude is None:
                        continue  # ignora se não tem localização

                    dist = calcular_distancia(
                        lat_filtro,
                        lon_filtro,
                        addr.latitude,
                        addr.longitude,
                    )

                    if dist <= distancia_max_km:
                        filtrados.append(p)

                produtos = filtrados

            # etapa 4: ordenar
            if order_by == "preco":
                produtos.sort(key=lambda p: p.preco)

            elif order_by == "distancia" and lat_filtro and lon_filtro:
                produtos.sort(
                    key=lambda p: calcular_distancia(
                        lat_filtro,
                        lon_filtro,
                        p.banca.address.latitude,
                        p.banca.address.longitude,
                    )
                )

            # transformar para DTO
            produtos_result = [
                ProdutoRead(
                    id=p.id,
                    nome=p.nome,
                    preco=p.preco,
                    imagem=p.imagem,
                    banca_id=p.banca_id,
                    created_at=p.created_at,
                    updated_at=p.updated_at,
                )
                for p in produtos
            ]

        # --------------------------------------------------------
        # 3. Buscar BANCAS
        # --------------------------------------------------------
        if tipo in ("banca", "all"):
            bancas = self.banca_repo.get_all()

            # etapa 1: filtrar pelo nome
            bancas = [b for b in bancas if termo.lower() in b.nome.lower()]

            # etapa 2: filtrar por distância (se tiver coordenadas)
            if distancia_max_km is not None and lat_filtro and lon_filtro:
                filtradas = []
                for b in bancas:
                    addr = b.address
                    if addr.latitude is None or addr.longitude is None:
                        continue

                    dist = calcular_distancia(
                        lat_filtro,
                        lon_filtro,
                        addr.latitude,
                        addr.longitude,
                    )

                    if dist <= distancia_max_km:
                        filtradas.append(b)

                bancas = filtradas

            # etapa 3: ordenar por distância
            if order_by == "distancia" and lat_filtro and lon_filtro:
                bancas.sort(
                    key=lambda b: calcular_distancia(
                        lat_filtro,
                        lon_filtro,
                        b.address.latitude,
                        b.address.longitude,
                    )
                )

            # transformar para DTO
            bancas_result = [
                BancaRead(
                    id=b.id,
                    nome=b.nome,
                    descricao=b.descricao,
                    horario_funcionamento=b.horario_funcionamento,
                    supplier_id=b.supplier_id,
                    address_id=b.address_id,
                    created_at=b.created_at,
                    updated_at=b.updated_at,
                )
                for b in bancas
            ]

        # --------------------------------------------------------
        # 4. Retorno final no formato SearchResponse
        # --------------------------------------------------------
        return SearchResponse(
            query=termo,
            produtos=produtos_result,
            bancas=bancas_result,
        )
