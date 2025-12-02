from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_criar_banca_deve_retornar_201():
    payload = {
        "nome": "Banca TDD",
        "descricao": "Banca criada no TDD",
        "horario_funcionamento": "08h - 18h",
        "supplier_id": "SUP-123",
        "address": {
            "street": "Rua Teste",
            "number": "123",
            "city": "Cidade X",
            "state": "ST",
            "zip_code": "00000-000",
        },
    }

    response = client.post("/bancas/", json=payload)

    assert response.status_code == 201
    body = response.json()

    assert body["nome"] == payload["nome"]
    assert body["supplier_id"] == payload["supplier_id"]
    assert "id" in body
    assert "address_id" in body
    assert "created_at" in body
    assert "updated_at" in body


def test_listar_bancas_deve_retornar_lista():
    response = client.get("/bancas/")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)

    if data:
        assert "id" in data[0]
        assert "nome" in data[0]
        assert "supplier_id" in data[0]


def test_obter_banca_inexistente():
    response = client.get("/bancas/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Banca não encontrada."


def test_deletar_banca():
    payload = {
        "nome": "Banca Delete TDD",
        "supplier_id": "SUP-999",
        "address": {
            "street": "Rua Apagar",
            "number": "50",
            "city": "Cidade Y",
            "state": "ST",
            "zip_code": "11111-111",
        },
    }

    created = client.post("/bancas/", json=payload).json()
    banca_id = created["id"]

    delete_resp = client.delete(f"/bancas/{banca_id}")
    assert delete_resp.status_code == 204

    get_resp = client.get(f"/bancas/{banca_id}")
    assert get_resp.status_code == 404
