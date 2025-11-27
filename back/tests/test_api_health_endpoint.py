from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_health_endpoint():
    """
    Verifica o comportamento do endpoint de saúde da aplicação.

    Este teste garante que o serviço responda corretamente, retornando os
    campos esperados e indicando operação normal do sistema.
    """
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "ok"
    assert "timestamp" in data
    assert "version" in data
