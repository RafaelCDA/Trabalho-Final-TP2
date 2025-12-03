from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from uuid import UUID

# ============================================================
# BASE
# ============================================================
class SupplierBase(BaseModel):
    nome: str = Field(..., description="Nome do fornecedor")
    email: EmailStr = Field(..., description="E-mail de contato")
    cidade: str = Field(..., description="Cidade de atuação")
    descricao: Optional[str] = Field(None, description="Descrição ou biografia")

# ============================================================
# CREATE
# ============================================================
class SupplierCreate(SupplierBase):
    pass

# ============================================================
# UPDATE (Faltava esta classe!)
# ============================================================
class SupplierUpdate(BaseModel):
    nome: Optional[str] = Field(None, description="Nome do fornecedor")
    email: Optional[EmailStr] = Field(None, description="E-mail de contato")
    cidade: Optional[str] = Field(None, description="Cidade de atuação")
    descricao: Optional[str] = Field(None, description="Descrição ou biografia")

# ============================================================
# READ (RESPONSE)
# ============================================================
class SupplierRead(SupplierBase):
    id: str  # Mudamos para str para evitar problemas de serialização UUID
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True