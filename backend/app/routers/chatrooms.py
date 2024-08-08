from fastapi import APIRouter
from typing import Union
from pydantic import BaseModel

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from app.routers import crud, database, models, schema

from typing import List


router = APIRouter(
	prefix="/chatrooms",
    tags=["chatrooms"]
)

# class Item(BaseModel):
#     name: str
#     description: Union[str, None] = None
#     price: float

class ChatRoom(BaseModel):
    roomId: int
    roomName: str

class ChatRoomRequest(BaseModel):
    userId: int
    urls: List[str]

class ChatRoomResponse(BaseModel):
    roomId:int

# @router.get("/")
# async def read_root():
#     return "This is root path from MyAPI"

# @router.get("/items/{item_id}")
# async def read_item(item_id: int, q: Union[str,  None] = None):
#     return {"item_id": item_id, "q": q}

# @router.post("/items/")
# async def create_item(item: Item):
#     return item

# @router.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     result = {"item_id": item_id, **item.dict()}

# @router.delete("/items/{item_id}")
# def delete_item(item_id: int):
#     return {"deleted": item_id}

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.on_event("startup")
def startup_event():
    database.create_tables()

# @router.post("/")
# async def create_chatroom(chatroom: schema.ChatRoomCreate, 
#                           db: Session = Depends(get_db)):
#     db_chatroom = crud.create_chatroom(db, chatroom)
#     db_chatroom["roomId"] = db_chatroom.pop["room_id"]
#     return db_chatroom

@router.post("/", response_model=ChatRoomResponse)
async def create_chatroom(request: ChatRoomRequest, 
                          chatroom: schema.ChatRoomCreate, 
                          db: Session = Depends(get_db)):
    #
    # Call userId = request.userId CRUD fuction
    #
    userId = 'test@ringchat.ai'

    #
    # Create chatroom record to DB
    #
    db_chatroom = crud.create_chatroom(db, chatroom)
    roomId = db_chatroom['room_id']

    chatrooms_data = {}
    chatrooms_data[userId].append({"roomId": roomId, "roomName": f'Chat Room {roomId}'})
    print(chatrooms_data)

    return {'roomId': roomId}