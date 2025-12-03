import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.core.database import Base


@pytest.fixture
def test_db():
    """
    Banco de dados isolado em memória para testes.

    - Garante que nenhum teste afete o ambiente real.
    - Tabelas são criadas e destruídas a cada execução.
    - Mantém o padrão de sessão utilizado no repositório.
    """

    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
