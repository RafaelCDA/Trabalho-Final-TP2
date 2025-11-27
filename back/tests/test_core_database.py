"""
Teste do módulo de configuração de banco de dados.

Este teste garante que o engine e a sessão sejam criados corretamente.
"""

from sqlalchemy.orm import Session
from sqlalchemy import text
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
    try:
        assert isinstance(db, Session)

        # Execução simples para validar comunicação com o banco
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            row = result.fetchone()

            assert row is not None
            assert row[0] == 1

    finally:
        db.close()
