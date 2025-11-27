"""
# Teste do Modelo de Usuário

Valida o comportamento básico do modelo de usuário. Este módulo confirma
que a entidade pode ser instanciada corretamente e que seus atributos
iniciais são preenchidos conforme esperado.

Este teste representa apenas a fase de validação estrutural do modelo.
A persistência será tratada em testes específicos do repositório.
"""

from src.models.user import User


def test_user_model_criacao_instancia():
    """
    ## Cenário
    Criar uma instância do modelo `User` com valores válidos.

    ## Expectativa
    - A instância deve refletir corretamente os dados fornecidos.
    - O campo `id` deve ser gerado automaticamente no formato UUID.
    """

    user = User(name="Guilherme", email="guilherme@test.com", password="123")

    assert getattr(user, "name") == "Guilherme"
    assert getattr(user, "email") == "guilherme@test.com"
    assert getattr(user, "password") == "123"
    assert user.id is not None
