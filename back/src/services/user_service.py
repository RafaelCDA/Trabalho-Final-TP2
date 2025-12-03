"""
Serviço responsável pelas operações de CRUD da entidade User.

Utiliza DTOs como interface de entrada e saída, aplica regras de negócio
mínimas e delega a persistência ao repositório.
"""

from typing import List, Optional, Literal, cast
from src.repositories.user_repository import UserRepository
from src.dto.user_dto import (
    UserCreateDTO,
    UserUpdateDTO,
    UserResponseDTO,
)


def _to_iso(value):
    """
    Garante compatibilidade com datetime ou string.

    Se o repositório retornar datetime:
        value.isoformat()

    Se o repositório retornar string:
        value
    """
    return value if isinstance(value, str) else value.isoformat()


class UserService:
    """
    Serviço para gerenciamento básico de usuários, oferecendo operações
    de criação, consulta, listagem, atualização e remoção.
    """

    def __init__(self, repository: UserRepository):
        """
        Inicializa o serviço com o repositório utilizado no acesso ao banco.

        Parâmetros
        ----------
        repository : UserRepository
            Instância responsável pelas operações de persistência.
        """
        self.repository = repository

    # ---------------------------------------------------------
    # CREATE
    # ---------------------------------------------------------
    def create_user(self, dto: UserCreateDTO) -> UserResponseDTO:
        """
        Cria um novo usuário aplicando validação simples de e-mail duplicado.
        """
        existing = self.repository.get_by_email(dto.email)
        if existing:
            raise ValueError("E-mail já cadastrado.")

        user = self.repository.create_user(
            name=dto.name,
            email=dto.email,
            password=dto.password,
            type=dto.type,
        )

        return UserResponseDTO(
            id=str(user.id),
            name=str(user.name),
            email=str(user.email),
            type=cast(Literal["user", "admin", "supplier"], str(user.type)),
            created_at=_to_iso(user.created_at),
            updated_at=_to_iso(user.updated_at),
        )

    # ---------------------------------------------------------
    # READ
    # ---------------------------------------------------------
    def get_user(self, user_id: str) -> Optional[UserResponseDTO]:
        """
        Retorna informações de um usuário pelo identificador.
        """
        user = self.repository.get_by_id(user_id)
        if not user:
            return None

        return UserResponseDTO(
            id=str(user.id),
            name=str(user.name),
            email=str(user.email),
            type=cast(Literal["user", "admin", "supplier"], str(user.type)),
            created_at=_to_iso(user.created_at),
            updated_at=_to_iso(user.updated_at),
        )

    # ---------------------------------------------------------
    # LIST
    # ---------------------------------------------------------
    def list_users(self) -> List[UserResponseDTO]:
        """
        Lista todos os usuários cadastrados no sistema.
        """
        users = self.repository.get_all()

        return [
            UserResponseDTO(
                id=str(u.id),
                name=str(u.name),
                email=str(u.email),
                type=cast(Literal["user", "admin", "supplier"], str(u.type)),
                created_at=_to_iso(u.created_at),
                updated_at=_to_iso(u.updated_at),
            )
            for u in users
        ]

    # ---------------------------------------------------------
    # UPDATE
    # ---------------------------------------------------------
    def update_user(
        self, user_id: str, dto: UserUpdateDTO
    ) -> Optional[UserResponseDTO]:
        """
        Atualiza os dados de um usuário existente.
        """
        user = self.repository.get_by_id(user_id)
        if not user:
            return None

        updated = self.repository.update_user(
            user_id=user_id,
            name=dto.name,
            email=dto.email,
            password=dto.password,
            type=dto.type,
        )

        if updated is None:
            return None

        return UserResponseDTO(
            id=str(updated.id),
            name=str(updated.name),
            email=str(updated.email),
            type=cast(Literal["user", "admin", "supplier"], str(updated.type)),
            created_at=_to_iso(updated.created_at),
            updated_at=_to_iso(updated.updated_at),
        )

    # ---------------------------------------------------------
    # DELETE
    # ---------------------------------------------------------
    def delete_user(self, user_id: str) -> None:
        """
        Remove o usuário associado ao identificador informado.
        """
        self.repository.delete_user(user_id)
