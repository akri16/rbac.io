from pydantic import BaseModel


class Log(BaseModel):
    timestamp: int
    msg: str