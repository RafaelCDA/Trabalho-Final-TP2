"""
Testes do repositório de usuários (CRUD completo).

Utiliza banco de dados isolado em memória.
"""

import uuid
from src.models.user import User
from src.repositories.user_repository import UserRepository


# --------------------------------------------------------------------
# CREATE
# --------------------------------------------------------------------


def test_create_user(test_db):
    repo = UserRepository(test_db)

    user = repo.create_user(
        name="Guilherme", email="guilherme@test.com", password="123"
    )

    assert isinstance(user, User)
    assert getattr(user, "id") is not None
    uuid.UUID(getattr(user, "id"), version=4)
    assert getattr(user, "name") == "Guilherme"
    assert getattr(user, "email") == "guilherme@test.com"


# --------------------------------------------------------------------
# READ
# --------------------------------------------------------------------


def test_get_user_by_id(test_db):
    repo = UserRepository(test_db)

    novo = repo.create_user("Ana", "ana@test.com", "456")
    encontrado = repo.get_by_id(getattr(novo, "id"))

    assert isinstance(encontrado, User)
    assert getattr(encontrado, "id") == getattr(novo, "id")


def test_get_user_by_email(test_db):
    repo = UserRepository(test_db)

    novo = repo.create_user("Luiz", "luiz@test.com", "789")
    encontrado = repo.get_by_email("luiz@test.com")

    assert isinstance(encontrado, User)
    assert getattr(encontrado, "email") == getattr(novo, "email")


def test_get_all_users(test_db):
    repo = UserRepository(test_db)

    repo.create_user("Ana", "ana2@test.com", "123")
    repo.create_user("Bruno", "bruno@test.com", "123")

    users = repo.get_all()

    assert isinstance(users, list)
    assert len(users) >= 2
    assert all(isinstance(u, User) for u in users)


# --------------------------------------------------------------------
# UPDATE
# --------------------------------------------------------------------


def test_update_user(test_db):
    repo = UserRepository(test_db)

    user = repo.create_user("Carlos", "carlos@test.com", "abc")

    atualizado = repo.update_user(
        user_id=getattr(user, "id"), name="Carlos Silva", email="carlos.silva@test.com"
    )

    assert isinstance(atualizado, User)
    assert getattr(atualizado, "name") == "Carlos Silva"
    assert getattr(atualizado, "email") == "carlos.silva@test.com"


# --------------------------------------------------------------------
# DELETE
# --------------------------------------------------------------------


def test_delete_user(test_db):
    repo = UserRepository(test_db)

    user = repo.create_user("Diego", "diego@test.com", "zzz")

    repo.delete_user(getattr(user, "id"))

    encontrado = repo.get_by_id(getattr(user, "id"))
    assert encontrado is None
