"""
Testes simples para a camada de serviço de usuários.

Valida operações básicas de CRUD e impede criação de usuários
com e-mail duplicado.
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
# CREATE
# ---------------------------------------------------------

def test_service_create_user(test_db):
    repo = UserRepository(test_db)
    service = UserService(repo)

    dto = UserCreateDTO(
        name="Guilherme",
        email="guilherme@test.com",
        password="123",
    )

    result = service.create_user(dto)

    assert isinstance(result, UserResponseDTO)
    assert result.name == "Guilherme"
    assert result.email == "guilherme@test.com"


def test_service_create_user_email_duplicado(test_db):
    repo = UserRepository(test_db)
    service = UserService(repo)

    dto = UserCreateDTO(
        name="Guilherme",
        email="duplicado@test.com",
        password="123",
    )

    service.create_user(dto)

    with pytest.raises(ValueError):
        service.create_user(dto)


# ---------------------------------------------------------
# READ
# ---------------------------------------------------------

def test_service_get_user(test_db):
    repo = UserRepository(test_db)
    service = UserService(repo)

    created = service.create_user(
        UserCreateDTO(name="Ana", email="ana@test.com", password="111")
    )

    found = service.get_user(created.id)

    assert isinstance(found, UserResponseDTO)
    assert found.id == created.id


def test_service_get_user_inexistente(test_db):
    repo = UserRepository(test_db)
    service = UserService(repo)

    result = service.get_user("nao-existe")
    assert result is None


# ---------------------------------------------------------
# LIST
# ---------------------------------------------------------

def test_service_list_users(test_db):
    repo = UserRepository(test_db)
    service = UserService(repo)

    service.create_user(UserCreateDTO(name="A", email="a@test.com", password="1"))
    service.create_user(UserCreateDTO(name="B", email="b@test.com", password="2"))

    users = service.list_users()

    assert isinstance(users, list)
    assert len(users) >= 2
    assert all(isinstance(u, UserResponseDTO) for u in users)


# ---------------------------------------------------------
# UPDATE
# ---------------------------------------------------------

def test_service_update_user(test_db):
    repo = UserRepository(test_db)
    service = UserService(repo)

    created = service.create_user(
        UserCreateDTO(name="Carlos", email="c@test.com", password="abc")
    )

    updated = service.update_user(
        created.id,
        UserUpdateDTO(name="Carlos Silva")
    )

    assert isinstance(updated, UserResponseDTO)
    assert updated.name == "Carlos Silva"


def test_service_update_user_inexistente(test_db):
    repo = UserRepository(test_db)
    service = UserService(repo)

    result = service.update_user("nao-existe", UserUpdateDTO(name="X"))
    assert result is None


# ---------------------------------------------------------
# DELETE
# ---------------------------------------------------------

def test_service_delete_user(test_db):
    repo = UserRepository(test_db)
    service = UserService(repo)

    created = service.create_user(
        UserCreateDTO(name="Diego", email="diego@test.com", password="zzz")
    )

    service.delete_user(created.id)

    assert service.get_user(created.id) is None


def test_service_delete_user_inexistente(test_db):
    repo = UserRepository(test_db)
    service = UserService(repo)

    service.delete_user("nao-existe")
