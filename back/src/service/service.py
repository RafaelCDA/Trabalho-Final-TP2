from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from src.models.message import Conversation, Message
from src.schemas.message import MessageCreate

class MessageService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_or_create_conversation(self, buyer_id: int, vendor_id: int) -> Conversation:
        """Busca ou cria uma conversa entre comprador e feirante"""
        conversation = self.db.query(Conversation).filter(
            and_(
                Conversation.buyer_id == buyer_id,
                Conversation.vendor_id == vendor_id
            )
        ).first()
        
        if not conversation:
            conversation = Conversation(buyer_id=buyer_id, vendor_id=vendor_id)
            self.db.add(conversation)
            self.db.commit()
            self.db.refresh(conversation)
        
        return conversation
    
    def send_message(self, conversation_id: int, sender_id: int, content: str) -> Message:
        """Envia uma mensagem na conversa"""
        message = Message(
            conversation_id=conversation_id,
            sender_id=sender_id,
            content=content
        )
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message
    
    def get_conversation_messages(self, conversation_id: int, user_id: int) -> List[Message]:
        """Busca mensagens de uma conversa (com verificação de permissão)"""
        conversation = self.db.query(Conversation).filter(
            Conversation.id == conversation_id,
            or_(
                Conversation.buyer_id == user_id,
                Conversation.vendor_id == user_id
            )
        ).first()
        
        if not conversation:
            return []
        
        return self.db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.sent_at.asc()).all()
    
    def get_user_conversations(self, user_id: int) -> List[Conversation]:
        """Busca todas as conversas do usuário"""
        return self.db.query(Conversation).filter(
            or_(
                Conversation.buyer_id == user_id,
                Conversation.vendor_id == user_id
            )
        ).order_by(Conversation.updated_at.desc()).all()