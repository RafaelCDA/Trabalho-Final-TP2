from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_criar_produto_endpoint():
    resp = client.post("/produtos", json={
        "nome": "Laranja",
        "preco": 4,
        "banca": "Banca 1",
        "lat": 0,
        "long": 0
    })

    assert resp.status_code == 201
    body = resp.json()
    assert body["nome"] == "Laranja"
    assert body["preco"] == 4

def test_busca_endpoint():
    # Criar produtos
    client.post("/produtos", json={
        "nome": "Samsung Apple TV",
        "preco": 4000,
        "banca": "Banca 2",
        "lat": 0,
        "long": 0
    })

    resp = client.get("/produtos/search?text=apple")
    assert resp.status_code == 200

    resultado = resp.json()
    assert len(resultado) >= 1
    assert "Apple" in resultado[0]["nome"] or "apple" in resultado[0]["nome"].lower()

