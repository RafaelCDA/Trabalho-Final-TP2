import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestMessageFlow:
    """Teste do fluxo completo de mensagens"""
    
    def test_complete_message_flow(self):
        """Teste do fluxo: enviar → listar → visualizar"""
        # Mock de autenticação
        with patch("src.api.dependencies.get_current_user") as mock_auth:
            mock_auth.return_value = {"id": 1, "email": "comprador@test.com"}
            
            # 1. Enviar mensagem
            response_send = client.post(
                "/api/v1/messages/conversations/2",
                json={"content": "Produto disponível?"},
                headers={"Authorization": "Bearer mock-token"}
            )
            
            # 2. Listar conversas
            response_list = client.get(
                "/api/v1/messages/conversations",
                headers={"Authorization": "Bearer mock-token"}
            )
            
            # 3. Ver histórico
            response_history = client.get(
                "/api/v1/messages/conversations/2", 
                headers={"Authorization": "Bearer mock-token"}
            )
            
            # Verificações
            assert response_send.status_code == 200
            assert response_list.status_code == 200
            assert response_history.status_code == 200
            
            # Verifica estrutura da resposta
            message_data = response_send.json()
            assert "id" in message_data
            assert "content" in message_data
            assert "sender_id" in message_data
            assert "sent_at" in message_data