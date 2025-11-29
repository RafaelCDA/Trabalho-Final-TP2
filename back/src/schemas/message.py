from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class MessageCreate(BaseModel):
    content: str

class MessageResponse(BaseModel):
    id: int
    sender_type: str
    sender_id: int
    content: str
    timestamp: datetime
    is_read: bool
    
    class Config:
        from_attributes = True

class ChatSummary(BaseModel):
    id: int
    user_id: int
    supplier_id: int
    other_party_id: int
    user_role: str  # 'user' ou 'supplier'
    last_message: Optional[str]
    last_message_time: Optional[datetime]
    unread_count: int
    
    class Config:
        from_attributes = True