from typing import Optional
from pydantic import BaseModel, Field, EmailStr

class UserSchema(BaseModel):
    fullname: Optional[str] = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Full Name",
                "email": "email@mail.com",
                "password": "password"
            }
        }

class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "email@mail.com",
                "password": "password"
            }
        }
