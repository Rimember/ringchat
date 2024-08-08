from sqlalchemy.orm import Session
from app.models.tables import ChatRooms
import datetime

def create_chatroom(db: Session, db_chatroom: ChatRooms):
    db.add(db_chatroom)
    db.commit()
    db.refresh(db_chatroom)
    return db_chatroom