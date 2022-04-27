
from fastapi import HTTPException
from app import constants
from app.models.role import Role
from app.models.user import User
from app.models.log import Log
from firebase_admin import auth, db


def check_dev(uid: str):
    curr_user = User(**db.reference(f'users/{uid}').get())

    if curr_user.role != Role.Developer:
        raise HTTPException(403, constants["DEV_FEAT"])

def get_all_logs(id: str):
    check_dev(id)
    logs = db.reference('logs').order_by_key().get()

    l = []
    for k, v in logs.items():
        log = dict()
        log['msg'] = v
        log['timestamp'] = k
        l.append(Log(**log))

    return l

                     


