"""
## DTOs: Pesquisa

Define os modelos utilizados para registrar pesquisas realizadas pelos usuários
e estruturar o retorno das buscas.
Os DTOs padronizam a validação dos dados enviados e recebidos pelas rotas,
permitindo consistência entre serviços e repositórios.
"""

from typing import List, Optional
from pydantic import BaseModel, Field

from src.dto.produto_dto import ProdutoRead
from src.dto.banca_dto import BancaRead


# ============================================================
# BASE
# ============================================================
class PesquisaBase(BaseModel):
    """
    Campos fundamentais de uma pesquisa realizada pelo usuário.
    """

    termo: str = Field(..., description="Texto pesquisado pelo usuário")
    latitude: Optional[float] = Field(
        None, description="Latitude do usuário no momento da pesquisa"
    )
    longitude: Optional[float] = Field(
        None, description="Longitude do usuário no momento da pesquisa"
    )


# ============================================================
# CREATE
# ============================================================
class PesquisaCreate(PesquisaBase):
    """
    Estrutura utilizada para registrar uma nova pesquisa.
    """

    pass


# ============================================================
# READ
# ============================================================
class PesquisaRead(PesquisaBase):
    """
    Dados retornados após o registro de uma pesquisa,
    incluindo identificador e data/hora.
    """

    id: int
    created_at: str

    class Config:
        from_attributes = True


# ============================================================
# SEARCH RESPONSE
# ============================================================
class SearchResponse(BaseModel):
    """
    Resultado consolidado de uma busca.
    Retorna listas de produtos e bancas relacionados ao termo pesquisado.
    """

    query: str = Field(..., description="Termo pesquisado")
    produtos: List[ProdutoRead] = Field(default_factory=list)
    bancas: List[BancaRead] = Field(default_factory=list)

    class Config:
        from_attributes = True
