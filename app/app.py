from ast import List
from ipaddress import ip_address
from fastapi import BackgroundTasks, Depends, FastAPI, Request, Response
from fastapi.params import Body
from fastapi.exceptions import HTTPException
import time
from firebase_admin import db
from fastapi.middleware.cors import CORSMiddleware
from app.firebase.admins import create_user, delete_user, get_user_with_id, get_users, update_role
from app.firebase.auth import FirebaseBearer
from app.firebase.common import login_client, log, check_valid_ip
from app.firebase.dev import block_user_ip, get_all_blocked_user_ips, get_all_logs, unblock_user_ip
from app.models.log import Log

from app.models.login import Login
from app.models.role import Role
from app.models.user import CreateUser, GetUser, GetUserWithToken, User
from starlette.responses import JSONResponse
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

@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    msg = f"{request.client} {request.method} {request.url} "
    response: Response = await call_next(request)
    msg += f"{response.status_code}"
    log(msg)
    return response

@app.middleware("http")
async def ip_validate_middleware(request: Request, call_next):
    try:
        check_valid_ip(request.client.host)
        response: Response = await call_next(request)
        return response
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content=e.detail)
    

@app.get("/")
async def root() -> dict:
    return {"message": "Hello World"}

@app.post("/login")
async def login(login: Login) -> GetUserWithToken:
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

@app.get("/logs", tags=['dev'], response_model = List[Log])
async def get_logs(id: str = Depends(FirebaseBearer())) -> List[Log]:
    return get_all_logs(id)

@app.put("/blocked_ip", tags=['dev'])
async def block_ip(ip: str, id: str = Depends(FirebaseBearer())) -> List[Log]:
    block_user_ip(id, ip_address(ip))
    return "Success"

@app.delete("/blocked_ip/{ip}", tags=['dev'])
async def unblock_ip(ip: str, id: str = Depends(FirebaseBearer())) -> List[Log]:
    unblock_user_ip(id, ip_address(ip))
    return "Success"

@app.get("/blocked_ips", tags=['dev'])
async def get_all_blocked_ips(id: str = Depends(FirebaseBearer())) -> List[str]:
    return get_all_blocked_user_ips(id)