from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import List
from src.models.message import Chat, Message

class MessageService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_or_create_chat(self, user_id: int, supplier_id: int) -> Chat:
        """Busca ou cria um chat entre usuário e fornecedor"""
        chat = self.db.query(Chat).filter(
            and_(
                Chat.user_id == user_id,
                Chat.supplier_id == supplier_id
            )
        ).first()
        
        if not chat:
            chat = Chat(user_id=user_id, supplier_id=supplier_id)
            self.db.add(chat)
            self.db.commit()
            self.db.refresh(chat)
        
        return chat
    
    def send_message(self, chat_id: int, sender_type: str, sender_id: int, content: str) -> Message:
        """Envia uma mensagem no chat"""
        message = Message(
            chat_id=chat_id,
            sender_type=sender_type,
            sender_id=sender_id,
            content=content
        )
        self.db.add(message)
        
        # Atualiza timestamp do chat
        chat = self.db.query(Chat).filter(Chat.id == chat_id).first()
        if chat:
            chat.updated_at = func.now()
        
        self.db.commit()
        self.db.refresh(message)
        return message
    
    def get_chat_messages(self, chat_id: int, current_user_id: int) -> List[Message]:
        """Busca mensagens de um chat (com verificação de permissão)"""
        chat = self.db.query(Chat).filter(
            Chat.id == chat_id,
            or_(
                Chat.user_id == current_user_id,
                Chat.supplier_id == current_user_id
            )
        ).first()
        
        if not chat:
            return []
        
        return self.db.query(Message).filter(
            Message.chat_id == chat_id
        ).order_by(Message.timestamp.asc()).all()
    
    def get_user_chats(self, user_id: int) -> List[dict]:
        """Busca todos os chats do usuário (como comprador ou fornecedor)"""
        chats = self.db.query(Chat).filter(
            or_(
                Chat.user_id == user_id,  # Chats onde é comprador
                Chat.supplier_id == user_id  # Chats onde é fornecedor
            )
        ).order_by(Chat.updated_at.desc()).all()
        
        result = []
        for chat in chats:
            last_message = self.db.query(Message).filter(
                Message.chat_id == chat.id
            ).order_by(Message.timestamp.desc()).first()
            
            # Conta mensagens não lidas
            unread_count = self.db.query(Message).filter(
                Message.chat_id == chat.id,
                Message.sender_id != user_id,  # Mensagens de outras pessoas
                Message.is_read == False
            ).count()
            
            # Determina o outro participante
            if user_id == chat.user_id:
                other_party_id = chat.supplier_id
                user_role = "user"
            else:
                other_party_id = chat.user_id
                user_role = "supplier"
            
            result.append({
                "id": chat.id,
                "user_id": chat.user_id,
                "supplier_id": chat.supplier_id,
                "other_party_id": other_party_id,
                "user_role": user_role,
                "last_message": last_message.content if last_message else "Nenhuma mensagem",
                "last_message_time": last_message.timestamp if last_message else None,
                "unread_count": unread_count
            })
        
        return result
    
    def mark_messages_as_read(self, chat_id: int, user_id: int):
        """Marca mensagens como lidas"""
        self.db.query(Message).filter(
            Message.chat_id == chat_id,
            Message.sender_id != user_id,  # Apenas mensagens de outras pessoas
            Message.is_read == False
        ).update({"is_read": True})
        self.db.commit()