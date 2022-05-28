from pydantic import BaseModel

class MessageFilter(BaseModel):
    sender_id : int
    receiver_id : int

class Message(MessageFilter):
    content : str

class User(BaseModel):
    email: str
    
class UserLogin(User):
    password: str

class UserCreate(UserLogin):
    first_name : str
    last_name : str

    class Config:
        orm_mode = True