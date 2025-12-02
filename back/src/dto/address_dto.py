from typing import Optional
from pydantic import BaseModel, Field


# -----------------------
# BASE (com campos comuns)
# -----------------------
class AddressBase(BaseModel):
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
    Dados necessários para registrar um endereço no sistema.
    """

    pass


# -----------------------
# UPDATE
# -----------------------
class AddressUpdate(BaseModel):
    """
    Campos opcionais que podem ser alterados em um endereço.
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
# READ (retorno)
# -----------------------
class AddressRead(AddressBase):
    id: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True
