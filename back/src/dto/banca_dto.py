"""
## DTOs: Banca

Define os modelos Pydantic utilizados para criação, atualização e leitura
de dados relacionados às bancas cadastradas pelos fornecedores.
Os DTOs padronizam a entrada e saída de informações entre rotas, serviços
e repositórios, garantindo validação e consistência estrutural.
"""

from typing import Optional
from pydantic import BaseModel, Field
from src.dto.address_dto import AddressCreate


# -----------------------
# BASE
# -----------------------
class BancaBase(BaseModel):
    """
    Campos fundamentais de uma banca, compartilhados entre
    operações de criação e leitura.
    """

    nome: str = Field(..., description="Nome da banca")
    descricao: Optional[str] = None
    horario_funcionamento: Optional[str] = None


# -----------------------
# CREATE
# -----------------------
class BancaCreate(BancaBase):
    """
    Estrutura necessária para registrar uma nova banca,
    incluindo o fornecedor responsável e os dados completos
    do endereço associado.
    """

    supplier_id: str = Field(..., description="ID do fornecedor")
    address: AddressCreate = Field(
        ..., description="Dados completos do endereço da banca"
    )


# -----------------------
# UPDATE
# -----------------------
class BancaUpdate(BaseModel):
    """
    Campos opcionais utilizados para atualização parcial
    de uma banca existente.
    """

    nome: Optional[str] = None
    descricao: Optional[str] = None
    horario_funcionamento: Optional[str] = None
    supplier_id: Optional[str] = None
    address_id: Optional[str] = None


# -----------------------
# READ
# -----------------------
class BancaRead(BancaBase):
    """
    Estrutura retornada pelas operações de leitura,
    incluindo identificadores e metadados de criação
    e atualização.
    """

    id: int
    supplier_id: str
    address_id: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True
