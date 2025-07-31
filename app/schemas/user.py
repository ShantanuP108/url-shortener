from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime

class UserRegister(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

    model_config = {
        "from_attributes": True
    }
