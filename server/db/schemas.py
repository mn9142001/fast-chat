from pydantic import BaseModel
class User(BaseModel):
    email: str
    # first_name : str
    # last_name : str

class UserBase(User):
    pass

class UserCreate(UserBase):
    password: str