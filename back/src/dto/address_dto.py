"""
## DTOs: Address

Define os modelos Pydantic utilizados para entrada, atualização
e retorno de dados relacionados a endereços.
Esses DTOs padronizam a validação e a estrutura de troca de informações
entre as camadas de rota, serviço e repositório.
"""

from typing import Optional
from pydantic import BaseModel, Field


# -----------------------
# BASE (campos comuns)
# -----------------------
class AddressBase(BaseModel):
    """
    Campos compartilhados entre os DTOs de criação, atualização e leitura.
    """

    street: str = Field(..., description="Logradouro")
    number: Optional[str] = Field(None, description="Número do imóvel")
    complement: Optional[str] = Field(None, description="Complemento")
    district: Optional[str] = Field(None, description="Bairro")
    city: str = Field(..., description="Cidade")
    state: str = Field(..., description="Estado/UF")
    zip_code: str = Field(..., description="CEP")
    latitude: Optional[float] = Field(None, description="Coordenada de latitude")
    longitude: Optional[float] = Field(None, description="Coordenada de longitude")


# -----------------------
# CREATE
# -----------------------
class AddressCreate(AddressBase):
    """
    Estrutura utilizada para cadastrar um novo endereço.
    """

    pass


# -----------------------
# UPDATE
# -----------------------
class AddressUpdate(BaseModel):
    """
    Campos opcionais para atualização parcial de um endereço.
    """

    street: Optional[str] = None
    number: Optional[str] = None
    complement: Optional[str] = None
    district: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


# -----------------------
# READ
# -----------------------
class AddressRead(AddressBase):
    """
    Estrutura retornada pelas operações de leitura,
    incluindo metadados de identificação e auditoria.
    """

    id: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True
