from typing import Optional
from pydantic import BaseModel, Field


# ============================================================
# BASE
# ============================================================


class ProdutoBase(BaseModel):
    nome: str = Field(..., description="Nome do produto")
    preco: float = Field(..., description="Preço do produto")
    imagem: Optional[str] = Field(
        None, description="URL da imagem ou caminho no sistema"
    )


# ============================================================
# CREATE
# ============================================================


class ProdutoCreate(ProdutoBase):
    """
    DTO utilizado para criação de um produto.
    """

    banca_id: int = Field(..., description="ID da banca à qual o produto pertence")


# ============================================================
# UPDATE
# ============================================================


class ProdutoUpdate(BaseModel):
    """
    DTO utilizado para atualização parcial de um produto.
    Todos os campos são opcionais para permitir PATCH.
    """

    nome: Optional[str] = None
    preco: Optional[float] = None
    imagem: Optional[str] = None
    banca_id: Optional[int] = None


# ============================================================
# READ (RESPONSE)
# ============================================================


class ProdutoRead(ProdutoBase):
    id: int
    banca_id: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True
