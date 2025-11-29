from fastapi import APIRouter, HTTPException, status, Depends, Header
from sqlalchemy.orm import Session
from typing import List, Optional

from src.models.database import get_db
from src.service.message_service import MessageService
from src.schemas.message import MessageCreate, MessageResponse, ChatSummary

router = APIRouter()

async def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token necessário")
    
    token = authorization.replace("Bearer ", "")
    if token != "mock-token":
        raise HTTPException(status_code=401, detail="Token inválido")
    
    # Mock - substitua pela lógica real de autenticação
    return {"id": 1, "email": "user@test.com", "user_type": "user"}

@router.post("/chats/{supplier_id}", response_model=MessageResponse)
async def send_message(
    supplier_id: int,
    message_data: MessageCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Enviar mensagem para um fornecedor"""
    service = MessageService(db)
    
    # Busca ou cria chat
    chat = service.get_or_create_chat(current_user["id"], supplier_id)
    
    # Envia mensagem (sender_type baseado no user_type do token)
    sender_type = current_user.get("user_type", "user")
    message = service.send_message(chat.id, sender_type, current_user["id"], message_data.content)
    
    return message

@router.get("/chats/{supplier_id}", response_model=List[MessageResponse])
async def get_chat_messages(
    supplier_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Buscar histórico de mensagens com um fornecedor"""
    service = MessageService(db)
    
    # Busca chat
    chat = service.get_or_create_chat(current_user["id"], supplier_id)
    
    # Marca mensagens como lidas
    service.mark_messages_as_read(chat.id, current_user["id"])
    
    # Busca mensagens
    messages = service.get_chat_messages(chat.id, current_user["id"])
    
    return messages

@router.get("/chats", response_model=List[ChatSummary])
async def get_user_chats(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Listar todos os chats do usuário"""
    service = MessageService(db)
    chats = service.get_user_chats(current_user["id"])
    
    return chats