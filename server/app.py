from fastapi import FastAPI, WebSocket, Request, HTTPException, Depends
from rtc.channels import FastSocket
import json
from db import schemas, models
from db.database import SessionLocal as Session
from orm import user as crud
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

@app.get('/login')
async def LogIn(request : Request):
    await FastSocket.group_send("group-1", json.dumps({"message" : "calling from login"}))

@app.websocket("/{id}")
async def websocket_endpoint(websocket: WebSocket, id):
    name:str = f"group-{id}"
    await FastSocket.group_add(name, websocket)
    

@app.post("/signup/")
async def create_user(user: schemas.UserCreate, db : Session =Depends(get_db)):
    session = db.query(models.UserModel).filter_by(email=user.email).first()
    
    # db_user = crud.get_user_by_email(db, email=user.email)
    # if db_user:
    #     raise HTTPException(status_code=400, detail="Email already registered")
    # return crud.create_user(db=db, user=user)