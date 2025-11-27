"""
Testes dos DTOs relacionados ao usuário.

Valida a estrutura básica, tipos esperados e comportamento mínimo dos
objetos de transferência de dados utilizados pela camada de API.
"""

import pytest
from pydantic import ValidationError
from src.dto.user_dto import (
    UserCreateDTO,
    UserUpdateDTO,
    UserResponseDTO,
    LoginDTO,
)


# UserCreateDTO


def test_user_create_dto_valido():
    dto = UserCreateDTO(
        name="Guilherme",
        email="guilherme@test.com",
        password="123",
    )

    assert dto.name == "Guilherme"
    assert dto.email == "guilherme@test.com"
    assert dto.password == "123"


def test_user_create_dto_email_invalido():
    with pytest.raises(ValidationError):
        UserCreateDTO(
            name="Guilherme",
            email="email-invalido",
            password="123",
        )


# UserUpdateDTO


def test_user_update_dto_parcial():
    dto = UserUpdateDTO(name="Novo Nome")

    assert dto.name == "Novo Nome"
    assert dto.email is None
    assert dto.password is None


def test_user_update_dto_email_invalido():
    with pytest.raises(ValidationError):
        UserUpdateDTO(email="email-invalido")


# UserResponseDTO


def test_user_response_dto_valido():
    dto = UserResponseDTO(
        id="123",
        name="Guilherme",
        email="guilherme@test.com",
    )

    assert dto.id == "123"
    assert dto.name == "Guilherme"
    assert dto.email == "guilherme@test.com"


def test_user_response_dto_email_invalido():
    with pytest.raises(ValidationError):
        UserResponseDTO(
            id="123",
            name="Guilherme",
            email="email-invalido",
        )


# LoginDTO


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
