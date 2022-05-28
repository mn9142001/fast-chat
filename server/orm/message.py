from db.database import SessionLocal
from db import models, schemas
from sqlalchemy import or_, and_


def create_message(message: schemas.Message, session: SessionLocal = SessionLocal()):
    print(message)
    db_message = models.Message(content =message.content, sender_id = message.sender_id, receiver_id = message.receiver_id)
    session.add(db_message)
    session.commit()
    session.refresh(db_message)
    return db_message

def get_user_messages(sender_id:int = 1, receiver_id:int = 2, session : SessionLocal = SessionLocal()):
    db_messages = session.query(models.Message).filter(or_(and_(models.Message.sender_id == sender_id, models.Message.receiver_id == receiver_id), and_(models.Message.receiver_id == sender_id, models.Message.sender_id == receiver_id))).all()
    return db_messages