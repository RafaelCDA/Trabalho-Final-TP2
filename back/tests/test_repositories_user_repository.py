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
        name="Guilherme", email="guilherme@test.com", password="123", type="user"
    )

    assert isinstance(user, User)
    assert getattr(user, "id") is not None
    uuid.UUID(getattr(user, "id"), version=4)
    assert getattr(user, "name") == "Guilherme"
    assert getattr(user, "email") == "guilherme@test.com"
    assert getattr(user, "type") == "user"
    assert getattr(user, "created_at") is not None
    assert getattr(user, "updated_at") is not None


def test_create_user_com_tipo_admin(test_db):
    repo = UserRepository(test_db)

    user = repo.create_user(
        name="Admin", email="admin@test.com", password="abc", type="admin"
    )

    assert isinstance(user, User)
    assert getattr(user, "type") == "admin"


def test_create_user_com_tipo_supplier(test_db):
    repo = UserRepository(test_db)

    user = repo.create_user(
        name="Fornecedor", email="for@test.com", password="abc", type="supplier"
    )

    assert isinstance(user, User)
    assert getattr(user, "type") == "supplier"


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

    antigo_updated_at = getattr(user, "updated_at")

    atualizado = repo.update_user(
        user_id=getattr(user, "id"),
        name="Carlos Silva",
        email="carlos.silva@test.com",
        type="admin",
    )

    assert isinstance(atualizado, User)
    assert getattr(atualizado, "name") == "Carlos Silva"
    assert getattr(atualizado, "email") == "carlos.silva@test.com"
    assert getattr(atualizado, "type") == "admin"

    # updated_at deve ter sido modificado
    assert getattr(atualizado, "updated_at") != antigo_updated_at


def test_update_user_inexistente(test_db):
    repo = UserRepository(test_db)

    resultado = repo.update_user("id_invalido", name="Teste")
    assert resultado is None


# --------------------------------------------------------------------
# DELETE
# --------------------------------------------------------------------


def test_delete_user(test_db):
    repo = UserRepository(test_db)

    user = repo.create_user("Diego", "diego@test.com", "zzz")

    repo.delete_user(getattr(user, "id"))

    encontrado = repo.get_by_id(getattr(user, "id"))
    assert encontrado is None


def test_delete_user_inexistente(test_db):
    repo = UserRepository(test_db)

    repo.delete_user("id_que_nao_existe")
