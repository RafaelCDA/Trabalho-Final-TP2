import pytest
import sys
import os

# Adiciona a pasta src ao Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, '..', 'src')
sys.path.insert(0, src_dir)

from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

class TestPrivateMessages:
    """Testes para o sistema de mensagens privadas - HU-08"""
    
    def test_send_message_unauthenticated_should_fail(self):
        """🔴 Teste 1: Usuário NÃO autenticado deve receber 401/403 (NÃO 404)"""
        response = client.post(
            "/api/v1/messages/conversations/1", 
            json={"content": "Olá, tenho uma dúvida"}
        )
        # DEVE FALHAR: Espera 401/403 mas recebe 404 (rota não existe)
        assert response.status_code in [401, 403]  # ← ESTE DEVE FALHAR!
    
    def test_send_message_authenticated_should_work(self):
        """🔴 Teste 2: Usuário autenticado deve conseguir enviar (status 200)"""
        # Mock de autenticação - mas a rota nem existe ainda
        response = client.post(
            "/api/v1/messages/conversations/2",
            json={"content": "Qual o preço?"},
            headers={"Authorization": "Bearer mock-token"}
        )
        # DEVE FALHAR: Espera 200 mas recebe 404
        assert response.status_code == 200  # ← ESTE DEVE FALHAR!
    
    def test_get_conversations_should_return_list(self):
        """🔴 Teste 3: Deve retornar lista de conversas"""
        response = client.get(
            "/api/v1/messages/conversations",
            headers={"Authorization": "Bearer mock-token"}
        )
        # DEVE FALHAR: Espera 200 mas recebe 404
        assert response.status_code == 200  # ← ESTE DEVE FALHAR!
        assert isinstance(response.json(), list)  # ← ESTE DEVE FALHAR!

def test_basic_always_passes():
    """✅ Este sempre passa para verificar o setup"""
    assert 1 + 1 == 2