from pydantic import BaseModel, EmailStr, Field
from app.models.role import Role


class User(BaseModel):
    name: str = Field(max_length=30, min_length=1)
    role: Role
    email: EmailStr

class CreateUser(User):
    password: str = Field(max_length=12, min_length=6)

class GetUser(User):
    id: str