from fastapi import APIRouter
from typing import Optional, Union
from pydantic import BaseModel

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from app.routers import crud, schema
from app import database
from app.models import tables
from typing import List

from datetime import datetime, timedelta

from app.models.tables import ChatRooms, Links, Vectors


router = APIRouter(
	prefix="/chatrooms",
    tags=["chatrooms"]
)

class ChatRoom(BaseModel):
    roomId: int
    roomName: str
    folderId: int
    created_time: Optional[datetime] = None

class ChatRoomRequest(BaseModel):
    userId: int
    urls: List[str]

class ChatRoomResponse(BaseModel):
    roomId: int

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ChatRoomResponse)
async def create_chatroom(request: ChatRoomRequest, 
                          db: Session = Depends(get_db)):
    
    now_utc = datetime.now()
    kst_offset = timedelta(hours=9)
    now_kst = now_utc + kst_offset
    
    chatroom = ChatRooms(user_id=request.userId,
                         created_time=now_kst,
                         folder_id=1,
                         room_name=f'New Chat\n{now_kst.strftime("%Y-%m-%d %H:%M:%S")}')
    
    db_chatroom = crud.create_chatroom(db, chatroom)
    roomId = db_chatroom.room_id

    return {"roomId": roomId}