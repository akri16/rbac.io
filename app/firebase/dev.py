
from ipaddress import IPv4Address
from typing import List
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

def block_user_ip(id: str, ip: IPv4Address):
    check_dev(id)
    keys = db.reference('blocked_ips').order_by_value().equal_to(ip.exploded).get().keys()
    if len(keys) == 0:
        db.reference('blocked_ips').push(ip.exploded)


def unblock_user_ip(id: str, ip: IPv4Address):
    check_dev(id)
    keys = list(db.reference('blocked_ips').order_by_value().equal_to(ip.exploded).get().keys())
    if len(keys) == 0:
        raise HTTPException(403, constants['IP_NOT_BLOCK'])
        
    db.reference(f'blocked_ips/{keys[0]}').delete()

def get_all_blocked_user_ips(id: str) -> List[str]: 
    check_dev(id)
    ips = db.reference('blocked_ips').get()
    return list(ips.values())

                     


