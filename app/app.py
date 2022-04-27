from ast import List
from fastapi import Depends, FastAPI
from fastapi.params import Body
from fastapi.exceptions import HTTPException
import time
from firebase_admin import db
from fastapi.middleware.cors import CORSMiddleware
from app.firebase.admins import create_user, delete_user, get_user_with_id, get_users, update_role
from app.firebase.auth import FirebaseBearer
from app.firebase.common import login_client

from app.models.login import Login
from app.models.role import Role
from app.models.user import CreateUser, GetUser, User

from typing import List


app = FastAPI(title="Rbacc.io Backend")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root() -> dict:
    return {"message": "Hello World"}

@app.post("/login")
async def login(login: Login) -> dict:
    return await login_client(login.email, login.password)

@app.post("/create_user", response_model=GetUser, tags=['admin']) 
async def create_user_account(user: CreateUser, id: str = Depends(FirebaseBearer())) -> GetUser:
    return create_user(id, user)

@app.put("/update_role", tags=['admin'])
async def update_user_role(role: Role, user_uid: str, id: str = Depends(FirebaseBearer())):
    update_role(id, user_uid, role)
    return "Success"

@app.get("/users", tags=['admin'], response_model=List[GetUser])
async def get_all_users(id: str = Depends(FirebaseBearer())) -> List[GetUser]:
    return get_users(id)

@app.get("/user/{user_id}", response_model=GetUser, tags=['admin'])
async def get_user(user_id: str, id: str = Depends(FirebaseBearer())) -> GetUser:
    return get_user_with_id(id, user_id)

@app.delete("/user/{user_id}", tags=['admin'])
async def delete_user_account(user_id: str, id: str = Depends(FirebaseBearer())) -> str:
    delete_user(id, user_id)
    return "Success"