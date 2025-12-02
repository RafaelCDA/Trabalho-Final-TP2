from typing import Optional
from pydantic import BaseModel, Field
from src.dto.address_dto import AddressCreate


class BancaBase(BaseModel):
    nome: str = Field(..., description="Nome da banca")
    descricao: Optional[str] = None
    horario_funcionamento: Optional[str] = None


class BancaCreate(BancaBase):
    supplier_id: str = Field(..., description="ID do fornecedor")
    address: AddressCreate = Field(
        ..., description="Dados completos do endereço da banca"
    )


class BancaUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    horario_funcionamento: Optional[str] = None
    supplier_id: Optional[str] = None
    address_id: Optional[str] = None


class BancaRead(BancaBase):
    id: int
    supplier_id: str
    address_id: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True
