"""
Data Transfer Objects (DTOs) relacionados à entidade User.

Os DTOs padronizam a entrada e saída de dados da camada de API,
garantindo validação consistente e evitando exposição direta dos
modelos ORM.
"""

from typing import Optional
from pydantic import BaseModel, EmailStr


class UserCreateDTO(BaseModel):
    """
    Estrutura utilizada para criação de usuários.

    Parâmetros
    ----------
    name : str
        Nome completo do usuário.
    email : EmailStr
        Endereço de e-mail válido.
    password : str
        Senha enviada pela API.

    Retorno
    -------
    Instância validada contendo os dados de criação.
    """

    name: str
    email: EmailStr
    password: str


class UserUpdateDTO(BaseModel):
    """
    Estrutura utilizada para atualização parcial de usuário.

    Parâmetros
    ----------
    name : str | None
        Nome atualizado, quando enviado.
    email : EmailStr | None
        E-mail atualizado, quando enviado.
    password : str | None
        Senha atualizada, quando enviada.

    Observações
    -----------
    Todos os campos são opcionais para permitir atualizações parciais.
    """

    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserResponseDTO(BaseModel):
    """
    Estrutura retornada pela API ao expor dados de um usuário.

    Parâmetros
    ----------
    id : str
        Identificador do usuário.
    name : str
        Nome completo cadastrado.
    email : EmailStr
        Endereço de e-mail cadastrado.

    Observações
    -----------
    A senha não é retornada neste DTO.
    """

    id: str
    name: str
    email: EmailStr


class LoginDTO(BaseModel):
    """
    Estrutura utilizada no processo de autenticação simples.

    Parâmetros
    ----------
    email : EmailStr
        E-mail cadastrado.
    password : str
        Senha correspondente.

    Retorno
    -------
    Instância validada para o fluxo de autenticação.
    """

    email: EmailStr
    password: str
