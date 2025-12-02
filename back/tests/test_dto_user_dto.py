"""
Testes dos DTOs relacionados ao usuário.

Valida estrutura, tipos e validações dos DTOs utilizados pela API.
"""

import pytest
from pydantic import ValidationError
from datetime import datetime
from src.dto.user_dto import (
    UserCreateDTO,
    UserUpdateDTO,
    UserResponseDTO,
    LoginDTO,
)

# -------------------------------------------------------------------
# UserCreateDTO
# -------------------------------------------------------------------


def test_user_create_dto_valido():
    dto = UserCreateDTO(
        name="Guilherme",
        email="guilherme@test.com",
        password="123",
        type="user",
    )

    assert dto.name == "Guilherme"
    assert dto.email == "guilherme@test.com"
    assert dto.password == "123"
    assert dto.type == "user"


def test_user_create_dto_email_invalido():
    with pytest.raises(ValidationError):
        UserCreateDTO(
            name="Guilherme",
            email="email-invalido",
            password="123",
            type="user",
        )


def test_user_create_dto_tipo_invalido():
    with pytest.raises(ValidationError):
        UserCreateDTO(
            name="Guilherme",
            email="valido@test.com",
            password="123",
            type="INVALIDO", # pyright: ignore[reportArgumentType]
        )


# -------------------------------------------------------------------
# UserUpdateDTO
# -------------------------------------------------------------------


def test_user_update_dto_parcial():
    dto = UserUpdateDTO(name="Novo Nome")

    assert dto.name == "Novo Nome"
    assert dto.email is None
    assert dto.password is None
    assert dto.type is None  # caso você permita atualizar type, se não existir remova


def test_user_update_dto_email_invalido():
    with pytest.raises(ValidationError):
        UserUpdateDTO(email="email-invalido")


# -------------------------------------------------------------------
# UserResponseDTO
# -------------------------------------------------------------------


def test_user_response_dto_valido():
    dto = UserResponseDTO(
        id="123",
        name="Guilherme",
        email="guilherme@test.com",
        type="user",
        created_at="2024-01-01T10:00:00",
        updated_at="2024-01-01T10:00:00",
    )

    assert dto.id == "123"
    assert dto.name == "Guilherme"
    assert dto.email == "guilherme@test.com"
    assert dto.type == "user"
    assert isinstance(dto.created_at, str) or isinstance(dto.created_at, datetime)
    assert isinstance(dto.updated_at, str) or isinstance(dto.updated_at, datetime)


def test_user_response_dto_email_invalido():
    with pytest.raises(ValidationError):
        UserResponseDTO(
            id="123",
            name="Guilherme",
            email="email-invalido",
            type="user",
            created_at="2024-01-01T10:00:00",
            updated_at="2024-01-01T10:00:00",
        )


# -------------------------------------------------------------------
# LoginDTO
# -------------------------------------------------------------------


def test_login_dto_valido():
    dto = LoginDTO(
        email="user@test.com",
        password="123",
    )

    assert dto.email == "user@test.com"
    assert dto.password == "123"


def test_login_dto_email_invalido():
    with pytest.raises(ValidationError):
        LoginDTO(email="invalido", password="abc")
