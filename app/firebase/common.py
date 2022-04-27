import os, time, httpx
from fastapi.exceptions import HTTPException
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db, auth
from ..constants import constants, login_endpoint


def init():
    cred = credentials.Certificate('app/firebase/service-account.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': os.getenv('DATABASE_URL')
    })



def verify_id_token(token: str):
    try:
        decoded_token = auth.verify_id_token(token)
    except Exception:
        return None
    
    if decoded_token:
        return decoded_token['uid']

def getUserDetails(id: str):
    user = db.reference(f'users/{id}').get()
    if user is None:
        raise HTTPException(status_code=403, detail=constants['USER_NOT_CREATED'])

    return user


async def login_client(email: str, password: str):
    data = {'email': email, 'password': password, 'returnSecureToken': True}

    async with httpx.AsyncClient() as client:
        r = await client.post(login_endpoint, json=data)
        return r.json()

def log(msg: str):
    curr = int(time.time())
    db.reference(f'logs/{curr}').set(msg)

def check_valid_ip(ip: str):
    keys = db.reference('blocked_ips').order_by_value().equal_to(ip).get().keys()
    if len(keys) != 0:
        raise HTTPException(403, constants['IP_BLOCKED'])
    