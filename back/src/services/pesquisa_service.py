"""
## Serviço: PesquisaService

Responsável pelas operações de busca dentro do sistema.

Este serviço oferece funcionalidades avançadas para:
- registrar pesquisas realizadas pelos usuários
- buscar produtos e bancas por termo
- aplicar filtros de preço máximo
- aplicar filtros de distância máxima (Haversine)
- ordenar resultados por distância ou preço
- combinar múltiplos filtros simultaneamente

A camada de serviços integra consultas nos repositórios e aplica
toda a lógica de negócio antes de retornar resultados estruturados.
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
    Calcula a distância entre dois pontos geográficos usando a fórmula de Haversine.

    Parâmetros
    ----------
    lat1 : float
        Latitude do primeiro ponto.
    lon1 : float
        Longitude do primeiro ponto.
    lat2 : float
        Latitude do segundo ponto.
    lon2 : float
        Longitude do segundo ponto.

    Retorno
    -------
    float
        Distância em quilômetros entre os dois pontos.
    """
    R = 6371  # raio médio da Terra em km

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
    """
    Serviço responsável pela lógica de busca e registro de pesquisas.

    Operações cobertas:
    - Registro da pesquisa realizada.
    - Busca de produtos e bancas por termo.
    - Filtros por preço máximo.
    - Filtros por distância (usando coordenadas GPS).
    - Ordenação por distância ou preço.
    """

    def __init__(self, db: Session):
        """
        Inicializa o serviço com instâncias dos repositórios usados.

        Parâmetros
        ----------
        db : Session
            Sessão ativa do SQLAlchemy compartilhada entre os repositórios.
        """
        self.db = db
        self.produto_repo = ProdutoRepository(db)
        self.banca_repo = BancaRepository(db)
        self.pesquisa_repo = PesquisaRepository(db)

    # --------------------------------------------------------
    # BUSCAR PRODUTOS E/OU BANCAS
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
        Executa uma busca com filtros opcionais de preço, distância e ordenação.

        Parâmetros
        ----------
        termo : str
            Texto pesquisado pelo usuário.
        tipo : str
            Tipo de dado buscado ("produto", "banca" ou "all").
        lat_user : float | None
            Latitude real do usuário (para registrar a pesquisa).
        lon_user : float | None
            Longitude real do usuário (para registrar a pesquisa).
        preco_max : float | None
            Limite máximo de preço permitido nos resultados.
        distancia_max_metros : float | None
            Distância máxima permitida (em metros) para filtrar resultados.
        order_by : str | None
            Critério de ordenação ("preco" ou "distancia").
        lat_ref : float | None
            Latitude alternativa para aplicar filtros de distância.
        lon_ref : float | None
            Longitude alternativa para aplicar filtros de distância.

        Retorno
        -------
        SearchResponse
            Resultado da busca com listas de produtos e bancas filtradas.
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

        # Se houver filtro de distância, converter METROS → KM
        distancia_max_km = (
            distancia_max_metros / 1000.0 if distancia_max_metros is not None else None
        )

        # Localização base para filtros e ordenações
        lat_filtro = lat_ref if lat_ref is not None else lat_user
        lon_filtro = lon_ref if lon_ref is not None else lon_user

        # --------------------------------------------------------
        # 2. Buscar PRODUTOS
        # --------------------------------------------------------
        if tipo in ("produto", "all"):
            produtos = self.produto_repo.get_all()

            # Filtrar por nome
            produtos = [p for p in produtos if termo.lower() in p.nome.lower()]

            # Filtrar por preço máximo
            if preco_max is not None:
                produtos = [p for p in produtos if p.preco <= preco_max]

            # Filtrar por distância
            if distancia_max_km is not None and lat_filtro and lon_filtro:
                filtrados = []
                for p in produtos:
                    addr = p.banca.address
                    if addr.latitude is None or addr.longitude is None:
                        continue

                    dist = calcular_distancia(
                        lat_filtro, lon_filtro, addr.latitude, addr.longitude
                    )

                    if dist <= distancia_max_km:
                        filtrados.append(p)

                produtos = filtrados

            # Ordenar
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

            # Converter para DTO
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

            # Filtrar por nome
            bancas = [b for b in bancas if termo.lower() in b.nome.lower()]

            # Filtrar por distância
            if distancia_max_km is not None and lat_filtro and lon_filtro:
                filtradas = []
                for b in bancas:
                    addr = b.address
                    if addr.latitude is None or addr.longitude is None:
                        continue

                    dist = calcular_distancia(
                        lat_filtro, lon_filtro, addr.latitude, addr.longitude
                    )

                    if dist <= distancia_max_km:
                        filtradas.append(b)

                bancas = filtradas

            # Ordenar por distância
            if order_by == "distancia" and lat_filtro and lon_filtro:
                bancas.sort(
                    key=lambda b: calcular_distancia(
                        lat_filtro,
                        lon_filtro,
                        b.address.latitude,
                        b.address.longitude,
                    )
                )

            # Converter para DTO
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
        # 4. Retorno no formato SearchResponse
        # --------------------------------------------------------
        return SearchResponse(
            query=termo,
            produtos=produtos_result,
            bancas=bancas_result,
        )
