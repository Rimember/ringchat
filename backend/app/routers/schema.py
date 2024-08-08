from pydantic import BaseModel

# class ItemBase(BaseModel):
#     name: str
#     description: str
#     price: int

# class ItemCreate(ItemBase):
#     pass

# class Item(ItemBase):
#     id: int

#     class Config:
#         orm_mode = True

class ChatRoomBase(BaseModel):
    room_name: str
    #bookmark: bool
    #links: str

class ChatRoomCreate(ChatRoomBase):
    pass

class ChatRoom(ChatRoomBase):
    room_id: int

    class Config:
        orm_mode = True
