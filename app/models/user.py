from pydantic import BaseModel
from app.models.role import Role


class User(BaseModel):
    name: str
    role: Role
    email: str

class CreateUser(User):
    password: str

class GetUser(User):
    id: str