from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class MessageCreate(BaseModel):
    content: str

class MessageResponse(BaseModel):
    id: int
    sender_id: int
    content: str
    sent_at: datetime
    is_read: bool
    
    class Config:
        from_attributes = True