from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from . import common
from ..constants import constants


class FirebaseBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(FirebaseBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(FirebaseBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail=constants["INVALID_AUTH_SCHEME"])
            
            id = common.verify_id_token(credentials.credentials)
            if not id:
                raise HTTPException(status_code=403, detail=constants["INVALID_AUTH_CODE"])
            return id
        else:
            raise HTTPException(status_code=403, detail=constants["INVALID_AUTH_STATE"])