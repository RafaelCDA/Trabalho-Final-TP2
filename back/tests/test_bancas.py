from unittest.mock import MagicMock

from src.services.banca_service import BancaService
from src.dto.banca_dto import BancaCreate, BancaUpdate
from src.dto.address_dto import AddressCreate
from src.models.banca import Banca
from src.models.address import Address


def setup_service():
    banca_repo = MagicMock()
    address_repo = MagicMock()
    service = BancaService(banca_repo=banca_repo, address_repo=address_repo)
    return service, banca_repo, address_repo


# ============================================================
# CREATE
# ============================================================
def test_criar_banca_deve_retornar_banca_read():
    service, banca_repo, address_repo = setup_service()

    # ORM Address precisa de TODOS os campos opcionais do modelo
    address = Address(
        street="Rua Teste",
        number="123",
        complement=None,
        district=None,
        city="Cidade X",
        state="ST",
        zip_code="00000-000",
        latitude=None,
        longitude=None
    )
    address.id = "1"
    address_repo.create_address.return_value = address

    # ORM Banca também não aceita id no construtor
    banca = Banca(
        nome="Banca TDD",
        descricao="Banca criada",
        horario_funcionamento="08h - 18h",
        supplier_id="SUP-123",
        address_id="1",
    )
    banca.id = 1
    banca_repo.create_banca.return_value = banca

    dto = BancaCreate(
        nome="Banca TDD",
        descricao="Banca criada",
        horario_funcionamento="08h - 18h",
        supplier_id="SUP-123",
        address=AddressCreate(
            street="Rua Teste",
            number="123",
            complement=None,
            district=None,
            city="Cidade X",
            state="ST",
            zip_code="00000-000",
            latitude=None,
            longitude=None,
        )
    )

    result = service.create_banca(dto)

    assert result.id == 1
    assert result.nome == "Banca TDD"
    assert result.address_id == "1"


# ============================================================
# LIST
# ============================================================
def test_listar_bancas_deve_retornar_lista():
    service, banca_repo, _ = setup_service()

    b1 = Banca(nome="B1", supplier_id="S1", address_id="A1")
    b1.id = 1

    b2 = Banca(nome="B2", supplier_id="S2", address_id="A2")
    b2.id = 2

    banca_repo.get_all.return_value = [b1, b2]

    result = service.list_bancas()

    assert len(result) == 2
    assert result[0].id == 1
    assert result[1].id == 2


# ============================================================
# GET
# ============================================================
def test_obter_banca_inexistente():
    service, banca_repo, _ = setup_service()

    banca_repo.get_by_id.return_value = None

    result = service.get_banca(999999)

    assert result is None


# ============================================================
# DELETE
# ============================================================
def test_deletar_banca():
    service, banca_repo, _ = setup_service()

    b = Banca(nome="Teste", supplier_id="S", address_id="ADDR1")
    b.id = 1
    banca_repo.get_by_id.return_value = b

    result = service.delete_banca(1)

    assert result is True
    banca_repo.delete_banca.assert_called_once()


# ============================================================
# UPDATE
# ============================================================
def test_atualizar_banca():
    service, banca_repo, _ = setup_service()

    old = Banca(nome="Antigo", supplier_id="S", address_id="A1")
    old.id = 1
    banca_repo.get_by_id.return_value = old

    new = Banca(nome="Novo", supplier_id="S", address_id="A1")
    new.id = 1
    banca_repo.update_banca.return_value = new

    result = service.update_banca(1, BancaUpdate(nome="Novo"))

    assert result is not None
    assert result.nome == "Novo"
