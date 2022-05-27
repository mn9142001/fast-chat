from .database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

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
    state = Column(Enum(MessageStateEnum))
