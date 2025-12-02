from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_criar_banca_deve_retornar_201():
    payload = {
        "nome": "Banca TDD",
        "localizacao": "Feira Central",
        "descricao": "Banca criada no TDD",
        "horario_funcionamento": "08h - 18h",
    }

    response = client.post("/bancas/", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["nome"] == payload["nome"]
    assert body["localizacao"] == payload["localizacao"]


def test_listar_bancas_deve_retornar_lista():
    response = client.get("/bancas/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_obter_banca_inexistente():
    response = client.get("/bancas/999")
    assert response.status_code == 404


def test_deletar_banca():
    # cria
    payload = {
        "nome": "Banca Delete TDD",
        "localizacao": "Feira Oeste",
    }
    created = client.post("/bancas/", json=payload).json()
    banca_id = created["id"]

    # deleta
    response = client.delete(f"/bancas/{banca_id}")
    assert response.status_code == 204

    # confirma que não existe
    response = client.get(f"/bancas/{banca_id}")
    assert response.status_code == 404
