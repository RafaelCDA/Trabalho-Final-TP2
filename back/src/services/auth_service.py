"""
## Serviço: AuthService

Responsável pela autenticação simples de usuários através de e-mail e senha.
Utiliza DTOs para validação de entrada e resposta, e delega consultas ao
UserRepository.
Este serviço não implementa hashing de senha — apenas validações diretas,
adequado para ambientes controlados ou protótipos.
"""

from typing import Literal, cast
from src.dto.user_dto import LoginDTO, UserResponseDTO
from src.repositories.user_repository import UserRepository


def _to_iso(value):
    """
    Converte um datetime para string ISO 8601 caso necessário.

    Parâmetros
    ----------
    value : datetime | str
        Valor retornado pelo ORM.

    Retorno
    -------
    str
        Representação padrão ISO 8601.
    """
    return value if isinstance(value, str) else value.isoformat()


class AuthService:
    """
    Serviço responsável por operações de autenticação de usuários.
    Consulta o repositório para verificar credenciais e retorna um DTO
    contendo as informações do usuário autenticado.
    """

    def __init__(self, user_repository: UserRepository):
        """
        Inicializa o serviço com o repositório de usuários.

        Parâmetros
        ----------
        user_repository : UserRepository
            Instância de repositório utilizada para buscar usuários.
        """
        self.user_repository = user_repository

    # ---------------------------------------------------------
    # LOGIN
    # ---------------------------------------------------------
    def login_user(self, dto: LoginDTO) -> UserResponseDTO:
        """
        Realiza a autenticação simples de um usuário utilizando e-mail e senha.

        Parâmetros
        ----------
        dto : LoginDTO
            Dados fornecidos pelo cliente para autenticação, contendo
            e-mail e senha.

        Retorno
        -------
        UserResponseDTO
            Objeto contendo dados públicos do usuário autenticado.

        Exceções
        --------
        ValueError
            Lançado quando o e-mail não existe ou a senha está incorreta.
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
