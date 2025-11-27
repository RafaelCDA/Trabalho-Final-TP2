"""
Teste do módulo de configuração de banco de dados.

Este teste garante que o engine e a sessão sejam criados corretamente.
"""

from sqlalchemy.orm import Session
from src.core.database import engine, SessionLocal


def test_engine_deve_existir():
    """
    Cenário:
    - A aplicação deve prover um engine funcional.

    Expectativa:
    - O engine deve possuir atributo 'connect'.
    """
    assert hasattr(engine, "connect")


def test_sessao_deve_criar_conexao():
    """
    Cenário:
    - Abrir uma sessão de banco de dados.

    Expectativa:
    - A sessão deve ser instância de Session.
    - A sessão deve permitir operações básicas.
    """

    db = SessionLocal()

    assert isinstance(db, Session)

    # Tentativa de operação simples (ping no banco)
    conn = engine.connect()
    result = conn.execute("SELECT 1")

    assert result.fetchone()[0] == 1

    conn.close()
    db.close()
