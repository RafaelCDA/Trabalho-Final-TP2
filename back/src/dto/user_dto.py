"""
Data Transfer Objects (DTOs) relacionados à entidade User.

Os DTOs padronizam a entrada e saída de dados na camada de API,
garantindo validações consistentes e evitando exposição direta dos
modelos ORM.
"""

from typing import Optional, Literal
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
        Senha enviada para criação da conta.
    type : Literal["user", "admin", "supplier"]
        Tipo do usuário (ex.: "user", "admin", "supplier").

    Retorno
    -------
    UserCreateDTO
        Instância validada contendo os dados fornecidos para criação.
    """

    name: str
    email: EmailStr
    password: str
    type: Literal["user", "admin", "supplier"]


class UserUpdateDTO(BaseModel):
    """
    Estrutura utilizada para atualização parcial dos dados de um usuário.

    Parâmetros
    ----------
    name : str | None
        Nome atualizado, quando informado.
    email : EmailStr | None
        E-mail atualizado, quando informado.
    password : str | None
        Senha atualizada, quando informada.
    type : Literal["user", "admin", "supplier"] | None
        Tipo atualizado, quando informado.

    Observações
    -----------
    Todos os campos são opcionais para permitir atualizações parciais,
    seguindo o formato de PATCH.
    """

    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    type: Optional[Literal["user", "admin", "supplier"]] = None


class UserResponseDTO(BaseModel):
    """
    Estrutura retornada pela API ao expor informações de um usuário.

    Parâmetros
    ----------
    id : str
        Identificador único do usuário.
    name : str
        Nome completo.
    email : EmailStr
        Endereço de e-mail cadastrado.
    type : str
        Tipo do usuário (perfil de acesso).
    created_at : str
        Data de criação do registro.
    updated_at : str
        Data da última modificação.

    Observações
    -----------
    A senha nunca é retornada neste DTO.
    """

    id: str
    name: str
    email: EmailStr
    type: Literal["user", "admin", "supplier"]
    created_at: str
    updated_at: str


class LoginDTO(BaseModel):
    """
    Estrutura utilizada no fluxo de autenticação.

    Parâmetros
    ----------
    email : EmailStr
        E-mail cadastrado no sistema.
    password : str
        Senha correspondente ao usuário.

    Retorno
    -------
    LoginDTO
        Instância validada para autenticação.
    """

    email: EmailStr
    password: str
