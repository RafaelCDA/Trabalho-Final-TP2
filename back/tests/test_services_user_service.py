"""
Testes simples para a camada de serviço de usuários.

Valida operações básicas de CRUD, tipos de usuário
e impede criação de usuários com e-mail duplicado.
"""

import pytest
from src.services.user_service import UserService
from src.repositories.user_repository import UserRepository
from src.dto.user_dto import (
    UserCreateDTO,
    UserUpdateDTO,
    UserResponseDTO,
)


# ---------------------------------------------------------
# CREATE - testando tipos de usuário
# ---------------------------------------------------------


@pytest.mark.parametrize("user_type", ["user", "admin", "supplier"])
def test_service_create_user_types(test_db, user_type):
    repo = UserRepository(test_db)
    service = UserService(repo)

    dto = UserCreateDTO(
        name="Teste",
        email=f"{user_type}@test.com",
        password="123",
        type=user_type,
    )

    result = service.create_user(dto)

    assert isinstance(result, UserResponseDTO)
    assert result.type == user_type
    assert result.email == f"{user_type}@test.com"
    assert isinstance(result.created_at, str)
    assert isinstance(result.updated_at, str)


def test_service_create_user_email_duplicado(test_db):
    repo = UserRepository(test_db)
    service = UserService(repo)

    dto = UserCreateDTO(
        name="Guilherme",
        email="duplicado@test.com",
        password="123",
        type="user",
    )

    service.create_user(dto)

    with pytest.raises(ValueError):
        service.create_user(dto)


# ---------------------------------------------------------
# READ
# ---------------------------------------------------------


@pytest.mark.parametrize("user_type", ["user", "admin", "supplier"])
def test_service_get_user_with_types(test_db, user_type):
    repo = UserRepository(test_db)
    service = UserService(repo)

    created = service.create_user(
        UserCreateDTO(
            name="Ana",
            email=f"ana_{user_type}@test.com",
            password="111",
            type=user_type,
        )
    )

    found = service.get_user(created.id)

    assert isinstance(found, UserResponseDTO)
    assert found.id == created.id
    assert found.type == user_type


def test_service_get_user_inexistente(test_db):
    repo = UserRepository(test_db)
    service = UserService(repo)

    result = service.get_user("nao-existe")
    assert result is None


# ---------------------------------------------------------
# LIST
# ---------------------------------------------------------


def test_service_list_users_with_all_types(test_db):
    repo = UserRepository(test_db)
    service = UserService(repo)

    service.create_user(
        UserCreateDTO(name="A", email="a@test.com", password="1", type="user")
    )
    service.create_user(
        UserCreateDTO(name="B", email="b@test.com", password="2", type="admin")
    )
    service.create_user(
        UserCreateDTO(name="C", email="c@test.com", password="3", type="supplier")
    )

    users = service.list_users()

    assert isinstance(users, list)
    assert len(users) >= 3

    types = {u.type for u in users}

    assert "user" in types
    assert "admin" in types
    assert "supplier" in types


# ---------------------------------------------------------
# UPDATE
# ---------------------------------------------------------


@pytest.mark.parametrize("user_type", ["user", "admin", "supplier"])
def test_service_update_user_preserves_type(test_db, user_type):
    repo = UserRepository(test_db)
    service = UserService(repo)

    created = service.create_user(
        UserCreateDTO(
            name="Carlos",
            email=f"carlos_{user_type}@test.com",
            password="abc",
            type=user_type,
        )
    )

    updated = service.update_user(created.id, UserUpdateDTO(name="Carlos Silva"))

    assert isinstance(updated, UserResponseDTO)
    assert updated.name == "Carlos Silva"
    assert updated.type == user_type


def test_service_update_user_inexistente(test_db):
    repo = UserRepository(test_db)
    service = UserService(repo)

    result = service.update_user("nao-existe", UserUpdateDTO(name="X"))
    assert result is None


# ---------------------------------------------------------
# DELETE
# ---------------------------------------------------------


@pytest.mark.parametrize("user_type", ["user", "admin", "supplier"])
def test_service_delete_user_by_type(test_db, user_type):
    repo = UserRepository(test_db)
    service = UserService(repo)

    created = service.create_user(
        UserCreateDTO(
            name="Diego",
            email=f"diego_{user_type}@test.com",
            password="zzz",
            type=user_type,
        )
    )

    service.delete_user(created.id)

    assert service.get_user(created.id) is None


def test_service_delete_user_inexistente(test_db):
    repo = UserRepository(test_db)
    service = UserService(repo)

    service.delete_user("nao-existe")
