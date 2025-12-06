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
        """🔴 Teste 1: Usuário NÃO autenticado deve receber 401"""
        # ROTA CORRIGIDA: /chats em vez de /conversations
        response = client.post(
            "/api/v1/messages/chats/1",  # ← MUDOU AQUI
            json={"content": "Olá, tenho uma dúvida"}
        )
        assert response.status_code in [401, 403]
    
    def test_send_message_authenticated_should_work(self):
        """🔴 Teste 2: Usuário autenticado deve conseguir enviar"""
        # ROTA CORRIGIDA: /chats em vez de /conversations
        response = client.post(
            "/api/v1/messages/chats/2",  # ← MUDOU AQUI
            json={"content": "Qual o preço?"},
            headers={"Authorization": "Bearer mock-token"}
        )
        assert response.status_code == 200
    
    def test_get_conversations_should_return_list(self):
        """🔴 Teste 3: Deve retornar lista de conversas"""
        # ROTA CORRIGIDA: /chats em vez de /conversations
        response = client.get(
            "/api/v1/messages/chats",  # ← MUDOU AQUI
            headers={"Authorization": "Bearer mock-token"}
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)

def test_basic_always_passes():
    """✅ Este sempre passa para verificar o setup"""
    assert 1 + 1 == 2