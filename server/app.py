from fastapi import FastAPI, WebSocket, Request, HTTPException, Depends
from rtc.channels import FastSocket
import json
from db import schemas, models
from db.database import SessionLocal as Session
from orm import user as crud, message
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

# print(schemas.UserCreate({
#     "first_name": "ahmed",
#     "id": 2,
#     "email": "thelord.mido880@gmail.com",
#     "hashed_password": "$2b$12$3WFvwVsH5l1tl6ASxhn6euLz5vb2rvKTq7Isrc9/o2frnrnL4ro6y",
#     "created": "2022-05-28T05:17:57.368725",
#     "last_name": "naser"
# }))


@app.get('/login')
async def LogIn(request : Request):
    await FastSocket.group_send("group-1", json.dumps({"message" : "calling from login"}))

@app.websocket("/{id}")
async def websocket_endpoint(websocket: WebSocket, id):
    name:str = f"user-{id}"
    await FastSocket.group_add(name, websocket)
    

@app.post("/signup/")
async def create_user(user: schemas.UserCreate, db : Session =Depends(get_db)):
    _user = crud.get_user_by_email(user.email)
    if _user:
        raise HTTPException(status_code=403, detail="user with this email exists")
    return crud.create_user(db=db, user=user)

@app.get("/users/list")
async def get_contacts():
    return crud.get_all_users()

@app.get("/chat/{id}")
async def get_contacts(id : int):
    return {'user' : crud.get_user(id), 'messages' : message.get_user_messages(1,2)}

@app.post("/message/create/")
def send_message(_message : schemas.Message):
    return message.create_message(_message)

@app.post("/login/")
async def login(user : schemas.UserLogin):
    _user = crud.get_user_by_email(user.email)
    assert _user, "No such user"
    return crud.get_user_by_email(user.email)