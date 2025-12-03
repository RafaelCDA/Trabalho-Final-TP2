"""
## DTOs: Produto

Define as estruturas Pydantic utilizadas para criação, atualização
e leitura de produtos vinculados a uma banca.
Os DTOs garantem validação consistente e padronizam a troca de dados
entre rotas, serviços e repositórios.
"""

from typing import Optional
from pydantic import BaseModel, Field


# ============================================================
# BASE
# ============================================================
class ProdutoBase(BaseModel):
    """
    Campos essenciais de um produto, comuns às operações
    de criação e leitura.
    """

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
    Estrutura utilizada para registrar um novo produto.
    """

    banca_id: int = Field(..., description="ID da banca à qual o produto pertence")


# ============================================================
# UPDATE
# ============================================================
class ProdutoUpdate(BaseModel):
    """
    Estrutura utilizada para atualização parcial de um produto.
    Todos os campos são opcionais, permitindo requisições do tipo PATCH.
    """

    nome: Optional[str] = None
    preco: Optional[float] = None
    imagem: Optional[str] = None
    banca_id: Optional[int] = None


# ============================================================
# READ
# ============================================================
class ProdutoRead(ProdutoBase):
    """
    Estrutura retornada pelas operações de leitura
    contendo identificadores e dados de auditoria.
    """

    id: int
    banca_id: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True
