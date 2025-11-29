from fastapi import APIRouter, HTTPException, status, Depends, Header
from sqlalchemy.orm import Session
from typing import List, Optional

from src.models.database import get_db
from src.service.message_service import MessageService
from src.schemas.message import MessageCreate, MessageResponse

router = APIRouter()

# Autenticação mock (substitua pela sua real)
async def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token necessário")
    
    token = authorization.replace("Bearer ", "")
    if token != "mock-token":
        raise HTTPException(status_code=401, detail="Token inválido")
    
    return {"id": 1, "email": "user@test.com"}

@router.post("/conversations/{vendor_id}", response_model=MessageResponse)
async def send_message(
    vendor_id: int,
    message_data: MessageCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Enviar mensagem real para um feirante"""
    service = MessageService(db)
    
    # Busca ou cria conversa
    conversation = service.get_or_create_conversation(current_user["id"], vendor_id)
    
    # Envia mensagem
    message = service.send_message(conversation.id, current_user["id"], message_data.content)
    
    return message

@router.get("/conversations/{vendor_id}", response_model=List[MessageResponse])
async def get_conversation(
    vendor_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Buscar histórico real de mensagens"""
    service = MessageService(db)
    
    conversation = service.get_or_create_conversation(current_user["id"], vendor_id)
    messages = service.get_conversation_messages(conversation.id, current_user["id"])
    
    return messages

@router.get("/conversations")
async def get_user_conversations(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Listar conversas reais do usuário"""
    service = MessageService(db)
    conversations = service.get_user_conversations(current_user["id"])
    
    # Formata resposta com informações úteis para o frontend
    result = []
    for conv in conversations:
        last_message = conv.messages[-1] if conv.messages else None
        
        result.append({
            "id": conv.id,
            "vendor_id": conv.vendor_id,
            "buyer_id": conv.buyer_id,
            "last_message": last_message.content if last_message else "Nenhuma mensagem",
            "last_message_time": last_message.sent_at if last_message else None,
            "unread_count": len([m for m in conv.messages if not m.is_read and m.sender_id != current_user["id"]])
        })
    
    return result