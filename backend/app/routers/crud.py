from sqlalchemy.orm import Session
# from app.routers.models import Item
# from app.routers.schema import ItemCreate
from app.routers.models import ChatRooms
from app.routers.schema import ChatRoomCreate


# def get_items(db: Session):
#     return db.query(Item).all()

# def get_item(db: Session, item_id: int):
#     return db.query(Item).filter(Item.id == item_id).first()

# def create_item(db: Session, item: ItemCreate):
#     db_item = Item(**item.dict())
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item

# def update_item(db: Session, item: Item, updated_item: ItemCreate):
#     for key, value in updated_item.dict().items():
#         setattr(item, key, value)
#     db.commit()
#     db.refresh(item)
#     return item

# def delete_item(db: Session, item: Item):
#     db.delete(item)
#     db.commit()

def create_chatroom(db: Session, chatroom: ChatRoomCreate):
    db_chatroom = ChatRooms(**chatroom.model_dump())
    db.add(db_chatroom)
    db.commit()
    db.refresh(db_chatroom)
    return db_chatroom