"""
Testes do AuthService em sua forma mais simples.

Valida o fluxo básico de autenticação:
- login bem-sucedido
- email inexistente
- senha incorreta
"""

import pytest
from src.services.auth_service import AuthService
from src.repositories.user_repository import UserRepository
from src.dto.user_dto import LoginDTO, UserResponseDTO


def test_auth_service_login_sucesso(test_db):
    repo = UserRepository(test_db)
    auth = AuthService(repo)

    # criar usuário previamente
    repo.create_user(
        name="Guilherme",
        email="guilherme@test.com",
        password="123",
    )

    dto = LoginDTO(email="guilherme@test.com", password="123")
    result = auth.login_user(dto)

    assert isinstance(result, UserResponseDTO)
    assert result.email == "guilherme@test.com"


def test_auth_service_email_inexistente(test_db):
    repo = UserRepository(test_db)
    auth = AuthService(repo)

    dto = LoginDTO(email="naoexiste@test.com", password="123")

    with pytest.raises(ValueError):
        auth.login_user(dto)


def test_auth_service_senha_incorreta(test_db):
    repo = UserRepository(test_db)
    auth = AuthService(repo)

    # criar usuário
    repo.create_user(
        name="Guilherme",
        email="user@test.com",
        password="senha-correta",
    )

    dto = LoginDTO(email="user@test.com", password="errada")

    with pytest.raises(ValueError):
        auth.login_user(dto)
