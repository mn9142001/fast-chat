from rtc.channels import FastSocket
from .database import Base, SessionLocal
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Enum, event
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from asgiref.sync import async_to_sync
import json
from datetime import date, datetime

class MessageStateEnum(enum.Enum):
    sent = 1
    received = 2
    seen = 3

class BaseModel(Base):
    __abstract__= True
    id = Column(Integer, primary_key=True)

class UserModel(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String)
    created = Column(DateTime, default=datetime.utcnow)
    hashed_password = Column(String)

class Message(BaseModel):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    receiver_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    sender = relationship("UserModel", foreign_keys=sender_id)
    receiver = relationship("UserModel", foreign_keys=receiver_id)
    content = Column(String)
    created = Column(DateTime, default=datetime.utcnow)
    state = Column(Enum(MessageStateEnum), default=MessageStateEnum.sent)

def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    elif isinstance(obj, MessageStateEnum):
        return 1
    raise TypeError ("Type %s not serializable" % type(obj))


@event.listens_for(Message, 'after_insert')
def after_message(mapper, connection, instance):
    async_to_sync(FastSocket.group_send)(
        f"user-{instance.receiver_id}", json.dumps({"newMessage" : {c.name: getattr(instance, c.name) for c in instance.__table__.columns}}, default=json_serial)
    )
