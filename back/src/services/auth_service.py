"""
Serviço responsável pela autenticação simples de usuários.

Executa validações básicas utilizando DTOs como interface e
consulta o repositório para verificar credenciais.
"""

from typing import Literal, cast
from src.dto.user_dto import LoginDTO, UserResponseDTO
from src.repositories.user_repository import UserRepository


def _to_iso(value):
    """Permite receber datetime ou string."""
    return value if isinstance(value, str) else value.isoformat()


class AuthService:
    """
    Fornece operações de autenticação simples utilizando e-mail e senha.
    """

    def __init__(self, user_repository: UserRepository):
        """
        Parâmetros
        ----------
        user_repository : UserRepository
            Repositório utilizado para acesso aos dados de usuário.
        """
        self.user_repository = user_repository

    # ---------------------------------------------------------
    # LOGIN
    # ---------------------------------------------------------
    def login_user(self, dto: LoginDTO) -> UserResponseDTO:
        """
        Realiza autenticação simples de usuário baseado em e-mail e senha.

        Exceções
        --------
        ValueError
            Quando o e-mail não existe ou a senha está incorreta.
        """
        user = self.user_repository.get_by_email(dto.email)
        if not user:
            raise ValueError("E-mail não encontrado.")

        if str(user.password) != dto.password:
            raise ValueError("Senha incorreta.")

        return UserResponseDTO(
            id=str(user.id),
            name=str(user.name),
            email=str(user.email),
            type=cast(Literal["user", "admin", "supplier"], str(user.type)),
            created_at=_to_iso(user.created_at),
            updated_at=_to_iso(user.updated_at),
        )
