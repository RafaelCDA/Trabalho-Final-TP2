"""
# Testes do Modelo de Usuário

Valida o comportamento do modelo de usuário, incluindo a criação
de instâncias com diferentes tipos permitidos e a rejeição de valores inválidos.

Cada teste garante que o modelo reflita corretamente as regras de domínio.
"""

import pytest
from src.models.user import User


def test_user_model_criacao_tipo_user():
    """
    ## Cenário
    Criar uma instância do modelo `User` com type="user".

    ## Expectativa
    - O tipo deve ser armazenado corretamente.
    - A instância deve ser válida.
    """

    user = User(name="João", email="joao@test.com", password="123", type="user")

    assert user.type == "user"
    assert user.id is not None


def test_user_model_criacao_tipo_admin():
    """
    ## Cenário
    Criar uma instância do modelo `User` com type="admin".

    ## Expectativa
    - O tipo deve ser armazenado corretamente.
    """

    user = User(name="Maria", email="maria@test.com", password="123", type="admin")

    assert user.type == "admin"


def test_user_model_criacao_tipo_supplier():
    """
    ## Cenário
    Criar uma instância do modelo `User` com type="supplier".

    ## Expectativa
    - O tipo deve ser atribuído sem erros.
    """

    user = User(
        name="Fornecedor", email="fornecedor@test.com", password="123", type="supplier"
    )

    assert user.type == "supplier"


def test_user_model_tipo_invalido():
    """
    ## Cenário
    Criar uma instância do modelo `User` com type inválido.

    ## Expectativa
    - Deve ocorrer um erro antes da criação válida da entidade.
    """

    with pytest.raises(Exception):
        User(
            name="Invalido", email="inv@test.com", password="123", type="qualquercoisa"
        )
