from fastapi import HTTPException
from app import constants
from app.models.role import Role
from app.models.user import CreateUser, GetUser, User
from firebase_admin import auth, db
from ..constants import constants


def check_admin(uid: str):
    curr_user = User(**db.reference(f'users/{uid}').get())

    if curr_user.role == Role.user:
        raise HTTPException(403, constants["ADMIN_FEAT"])

def create_user(uid: str, user: CreateUser):
    check_admin(uid)

    try:
        created_user = auth.create_user(email=user.email, display_name=user.name, password=user.password)
        user = User(**user.dict())
        db.reference(f'users/{created_user.uid}').set(user.dict())
        get_user = user.dict()
        get_user['id'] = created_user.uid
        return GetUser(**get_user)
    except auth.EmailAlreadyExistsError:
        raise HTTPException(409, constants['USER_EXISTS'])


def get_users(uid: str):
    check_admin(uid)
    users = db.reference('users').get()
    l = []
    for key in users:
        user = users[key]
        user['id'] = key
        l.append(GetUser(**user))
    return l

def update_role(uid: str, user_uid:str, role: Role):
    check_admin(uid)
    db.reference(f'users/{user_uid}/role').set(role._value_)

def get_user_with_id(uid: str, user_id: str):
    check_admin(uid)
    user = db.reference(f'users/{user_id}').get()
    user['id'] = user_id
    return GetUser(**user)

def delete_user(uid: str, user_id: str):
    check_admin(uid)
    auth.delete_user(user_id)
    db.reference(f'users/{user_id}').delete()