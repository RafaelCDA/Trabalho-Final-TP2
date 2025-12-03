"""
## Serviço: UserService

Responsável pelas operações de CRUD da entidade **User**.

A camada de serviços funciona como intermediária entre a API e o repositório,
validando dados, aplicando regras de negócio mínimas (como verificação de
e-mail duplicado) e retornando objetos DTO padronizados para consumo pela camada
de apresentação.
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
    Converte valores retornados pelo ORM para o formato ISO 8601.

    Parâmetros
    ----------
    value : datetime | str
        Data retornada pelo repositório.

    Retorno
    -------
    str
        Representação ISO 8601 da data.
    """
    return value if isinstance(value, str) else value.isoformat()


class UserService:
    """
    Serviço responsável pelo gerenciamento básico de usuários.

    Funcionalidades incluídas:
    - Criar usuários com validação de e-mail duplicado
    - Consultar usuários por ID
    - Listar todos os usuários
    - Atualizar dados parcialmente
    - Remover usuários
    """

    def __init__(self, repository: UserRepository):
        """
        Inicializa o serviço com o repositório de usuários.

        Parâmetros
        ----------
        repository : UserRepository
            Instância de repositório responsável pela persistência da entidade User.
        """
        self.repository = repository

    # ---------------------------------------------------------
    # CREATE
    # ---------------------------------------------------------
    def create_user(self, dto: UserCreateDTO) -> UserResponseDTO:
        """
        Cria um novo usuário aplicando validação simples de e-mail duplicado.

        Parâmetros
        ----------
        dto : UserCreateDTO
            Dados fornecidos para criação do usuário.

        Regras de Negócio
        -----------------
        - O e-mail informado não deve estar em uso.

        Exceções
        --------
        ValueError
            Quando já existe um usuário com o mesmo e-mail.

        Retorno
        -------
        UserResponseDTO
            DTO contendo os dados do usuário criado.
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
        Obtém os dados de um usuário pelo seu identificador.

        Parâmetros
        ----------
        user_id : str
            Identificador do usuário.

        Retorno
        -------
        UserResponseDTO | None
            DTO do usuário encontrado ou None caso não exista.
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

        Retorno
        -------
        List[UserResponseDTO]
            Lista de usuários em formato DTO.
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
        Atualiza parcialmente os dados de um usuário existente.

        Parâmetros
        ----------
        user_id : str
            Identificador do usuário a ser alterado.
        dto : UserUpdateDTO
            Campos a serem atualizados.

        Retorno
        -------
        UserResponseDTO | None
            DTO atualizado ou None se o usuário não existir.
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
        Remove um usuário do sistema.

        Parâmetros
        ----------
        user_id : str
            Identificador do usuário.

        Retorno
        -------
        None
            A operação não retorna valor.
        """
        self.repository.delete_user(user_id)
