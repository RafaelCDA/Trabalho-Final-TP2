"""
## DTOs: User

Define as estruturas utilizadas na criação, atualização, resposta e
autenticação de usuários.
Os DTOs garantem validações consistentes e evitam exposição direta dos
modelos ORM, padronizando a troca de dados entre APIs, serviços e
repositórios.
"""

from typing import Optional, Literal
from pydantic import BaseModel, EmailStr


# ============================================================
# CREATE
# ============================================================
class UserCreateDTO(BaseModel):
    """
    Estrutura utilizada para cadastrar um novo usuário.
    """

    name: str
    email: EmailStr
    password: str
    type: Literal["user", "admin", "supplier"]


# ============================================================
# UPDATE
# ============================================================
class UserUpdateDTO(BaseModel):
    """
    Estrutura utilizada para atualização parcial dos dados de um usuário.
    Todos os campos são opcionais, permitindo requisições do tipo PATCH.
    """

    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    type: Optional[Literal["user", "admin", "supplier"]] = None


# ============================================================
# READ / RESPONSE
# ============================================================
class UserResponseDTO(BaseModel):
    """
    Estrutura retornada pela API contendo as informações públicas de um usuário.
    A senha nunca é exposta neste DTO.
    """

    id: str
    name: str
    email: EmailStr
    type: Literal["user", "admin", "supplier"]
    created_at: str
    updated_at: str


# ============================================================
# LOGIN
# ============================================================
class LoginDTO(BaseModel):
    """
    Estrutura utilizada no fluxo de autenticação.
    """

    email: EmailStr
    password: str
