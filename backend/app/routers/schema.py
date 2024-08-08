from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ChatRoomBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    room_name: str
    user_id: int
    folder_id: int
    created_time: Optional[datetime] = None


class ChatRoomCreate(ChatRoomBase):
    room_id: int
    pass

class ChatRoom(ChatRoomBase):
    user_id: int
    folder_id: int
    created_time: Optional[datetime] = None

    class Config:
        from_attributes = True
