"""
DTOs relacionados à entidade User.

Versão mínima necessária para a fase RED do TDD. Os campos são
declarados apenas para permitir importação e type checking.
"""

from typing import Optional
from pydantic import BaseModel


class UserCreateDTO(BaseModel):
    """DTO mínimo para criação de usuário (fase RED)."""

    name: str
    email: str
    password: str


class UserUpdateDTO(BaseModel):
    """DTO mínimo para atualização parcial de usuário (fase RED)."""

    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class UserResponseDTO(BaseModel):
    """DTO mínimo para resposta de usuário (fase RED)."""

    id: str
    name: str
    email: str


class LoginDTO(BaseModel):
    """DTO mínimo para autenticação simples (fase RED)."""

    email: str
    password: str
