from typing import List, Optional
from pydantic import BaseModel, Field

from src.dto.produto_dto import ProdutoRead
from src.dto.banca_dto import BancaRead


# ============================================================
# BASE
# ============================================================


class PesquisaBase(BaseModel):
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
    DTO utilizado para registrar uma nova pesquisa feita pelo usuário.
    """

    pass


# ============================================================
# READ (RESPONSE DE UMA PESQUISA REGISTRADA)
# ============================================================


class PesquisaRead(PesquisaBase):
    id: int
    created_at: str

    class Config:
        from_attributes = True


# ============================================================
# SEARCH RESPONSE (RETORNO DA BUSCA)
# ============================================================


class SearchResponse(BaseModel):
    """
    Resultado da busca.
    Retorna listas separadas conforme o tipo pesquisado (produtos, bancas).
    """

    query: str = Field(..., description="Termo pesquisado")
    produtos: List[ProdutoRead] = Field(default_factory=list)
    bancas: List[BancaRead] = Field(default_factory=list)

    class Config:
        from_attributes = True
