from db.database import SessionLocal
from db import models, schemas
from passlib.hash import bcrypt

def password_hasher(password : str):
    return bcrypt.hash(password)

def check_password(user : models.UserModel, password : str):
    return bcrypt.verify(password, user.password)

def get_user(id : int):
    db = SessionLocal()
    user = db.query(models.UserModel).filter_by(id = id).first()
    return user

def create_user(db: SessionLocal, user: schemas.UserCreate):
    fake_hashed_password = password_hasher(user.password)
    db_user = models.UserModel(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# def get_user_by_email(db: SessionLocal, email: str):
#     raise BaseException("tezk")
