"""
Serviço responsável pelas operações de CRUD da entidade User.

Utiliza DTOs como interface de entrada e saída, aplica regras de negócio
mínimas e delega a persistência ao repositório.
"""

from typing import List, Optional
from src.repositories.user_repository import UserRepository
from src.dto.user_dto import (
    UserCreateDTO,
    UserUpdateDTO,
    UserResponseDTO,
)


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

        Parâmetros
        ----------
        dto : UserCreateDTO
            Estrutura contendo nome, e-mail e senha.

        Retorno
        -------
        UserResponseDTO
            Representação pública do usuário recém-criado.

        Exceções
        --------
        ValueError
            Quando o e-mail informado já está cadastrado.
        """
        existing = self.repository.get_by_email(dto.email)
        if existing:
            raise ValueError("E-mail já cadastrado.")

        user = self.repository.create_user(
            name=dto.name,
            email=dto.email,
            password=dto.password,
        )

        return UserResponseDTO(
            id=str(user.id),
            name=str(user.name),
            email=str(user.email),
        )

    # ---------------------------------------------------------
    # READ
    # ---------------------------------------------------------
    def get_user(self, user_id: str) -> Optional[UserResponseDTO]:
        """
        Retorna informações de um usuário pelo identificador.

        Parâmetros
        ----------
        user_id : str
            Identificador único do usuário.

        Retorno
        -------
        UserResponseDTO ou None
            Estrutura pública do usuário, caso exista.
        """
        user = self.repository.get_by_id(user_id)
        if not user:
            return None

        return UserResponseDTO(
            id=str(user.id),
            name=str(user.name),
            email=str(user.email),
        )

    # ---------------------------------------------------------
    # LIST
    # ---------------------------------------------------------
    def list_users(self) -> List[UserResponseDTO]:
        """
        Lista todos os usuários cadastrados no sistema.

        Retorno
        -------
        list[UserResponseDTO]
            Lista de usuários convertidos para DTO de resposta.
        """
        users = self.repository.get_all()

        return [
            UserResponseDTO(
                id=str(u.id),
                name=str(u.name),
                email=str(u.email),
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

        Parâmetros
        ----------
        user_id : str
            Identificador do usuário.
        dto : UserUpdateDTO
            Estrutura contendo campos opcionais para atualização.

        Retorno
        -------
        UserResponseDTO ou None
            Dados atualizados do usuário, se encontrado.
        """
        user = self.repository.get_by_id(user_id)
        if not user:
            return None

        updated = self.repository.update_user(
            user_id=user_id,
            name=dto.name,
            email=dto.email,
            password=dto.password,
        )

        if updated is None:
            return None

        return UserResponseDTO(
            id=str(updated.id),
            name=str(updated.name),
            email=str(updated.email),
        )

    # ---------------------------------------------------------
    # DELETE
    # ---------------------------------------------------------
    def delete_user(self, user_id: str) -> None:
        """
        Remove o usuário associado ao identificador informado.

        Parâmetros
        ----------
        user_id : str
            Identificador do usuário a ser removido.

        Retorno
        -------
        None
        """
        self.repository.delete_user(user_id)
