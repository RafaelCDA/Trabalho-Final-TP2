from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

class Chat(Base):  # Nome da tabela igual ao seu modelo
    __tablename__ = "chat"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Comprador
    supplier_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Feirante/Fornecedor
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan")

class Message(Base):  # Nome da tabela igual ao seu modelo
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chat.id"), nullable=False)
    sender_type = Column(String, nullable=False)  # 'user' ou 'supplier'
    sender_id = Column(Integer, nullable=False)  # ID do remetente
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    is_read = Column(Boolean, default=False)

    chat = relationship("Chat", back_populates="messages")