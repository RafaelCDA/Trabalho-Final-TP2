import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.database import Base
from src.services.pesquisa_service import PesquisaService
from src.models.address import Address
from src.models.banca import Banca
from src.models.produto_model import Produto


# ============================================================
# FIXTURES
# ============================================================


@pytest.fixture
def db_session():
    """Cria um banco SQLite em memória para testes."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)

    session = TestingSessionLocal()
    yield session
    session.close()


@pytest.fixture
def setup_data(db_session):
    """
    Cria dados completos para testes:
    - 2 endereços
    - 2 bancas
    - 3 produtos
    """

    # Endereços
    addr1 = Address(
        street="Rua A",
        number="10",
        complement=None,
        district="Centro",
        city="Curitiba",
        state="PR",
        zip_code="00000-000",
        latitude=-25.4400,
        longitude=-49.2800,
    )

    addr2 = Address(
        street="Rua B",
        number="99",
        complement=None,
        district="Bairro Novo",
        city="Curitiba",
        state="PR",
        zip_code="11111-111",
        latitude=-25.4500,
        longitude=-49.3000,
    )

    db_session.add_all([addr1, addr2])
    db_session.commit()

    # Bancas
    banca1 = Banca(
        supplier_id="user1",
        address_id=addr1.id,
        nome="Banca do João",
        descricao="Frutas frescas",
    )

    banca2 = Banca(
        supplier_id="user2",
        address_id=addr2.id,
        nome="Banca da Maria",
        descricao="Hortaliças",
    )

    db_session.add_all([banca1, banca2])
    db_session.commit()

    # Produtos
    p1 = Produto(banca_id=banca1.id, nome="Tomate Italiano", preco=8.5)
    p2 = Produto(banca_id=banca1.id, nome="Tomate Cereja", preco=12.0)
    p3 = Produto(banca_id=banca2.id, nome="Banana Nanica", preco=6.0)

    db_session.add_all([p1, p2, p3])
    db_session.commit()

    return {
        "addr1": addr1,
        "addr2": addr2,
        "banca1": banca1,
        "banca2": banca2,
        "produtos": [p1, p2, p3],
    }


# ============================================================
# TESTES
# ============================================================


def test_busca_produtos_filtrar_preco(db_session, setup_data):
    service = PesquisaService(db_session)

    response = service.buscar(
        termo="tomate", tipo="produto", lat_user=-25.44, lon_user=-49.28, preco_max=10
    )

    assert len(response.produtos) == 1
    assert response.produtos[0].nome == "Tomate Italiano"


def test_busca_produtos_filtrar_distancia(db_session, setup_data):
    service = PesquisaService(db_session)

    # Endereço do usuário próximo à banca1, mas longe da banca2
    response = service.buscar(
        termo="tomate",
        tipo="produto",
        lat_user=-25.4400,
        lon_user=-49.2800,
        distancia_max_metros=500,  # 0.5 km
    )

    # Tomate está na banca1 (próxima)
    assert len(response.produtos) == 2
    assert all("Tomate" in p.nome for p in response.produtos)


def test_busca_ordenar_por_preco(db_session, setup_data):
    service = PesquisaService(db_session)

    response = service.buscar(
        termo="tomate",
        tipo="produto",
        lat_user=None,
        lon_user=None,
        order_by="preco",
    )

    precos = [p.preco for p in response.produtos]
    assert precos == sorted(precos)


def test_buscar_bancas_por_nome(db_session, setup_data):
    service = PesquisaService(db_session)

    response = service.buscar(
        termo="maria",
        tipo="banca",
        lat_user=None,
        lon_user=None,
    )

    assert len(response.bancas) == 1
    assert response.bancas[0].nome == "Banca da Maria"


def test_busca_combinada_produtos_e_bancas(db_session, setup_data):
    service = PesquisaService(db_session)

    response = service.buscar(
        termo="a",
        tipo="all",
        lat_user=None,
        lon_user=None,
    )

    assert len(response.produtos) > 0
    assert len(response.bancas) > 0


def test_registro_pesquisa_no_banco(db_session, setup_data):
    """Valida que a pesquisa foi registrada no histórico."""
    service = PesquisaService(db_session)

    service.buscar(
        termo="tomate",
        tipo="produto",
        lat_user=-25.44,
        lon_user=-49.28,
    )

    registros = service.pesquisa_repo.get_all()
    assert len(registros) == 1
    assert registros[0].termo == "tomate"
