from datetime import date, datetime
from pydantic import BaseModel, Field, EmailStr, ConfigDict


class ContactBase(BaseModel):
    name: str = Field(max_length=30)
    fullname: str = Field(max_length=30)
    email: EmailStr
    phone_number: str
    birthday: date
    description: str = Field(max_length=150)


class ContactResponse(ContactBase):
    id: int
    created_at: datetime
    created_at: datetime | None
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


class UserSchema(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6, max_length=8)


class UserResponse(BaseModel):
    id: int = 1
    username: str
    email: EmailStr
    avatar: str

    model_config = ConfigDict(from_attributes=True)


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'


class RequestEmail(BaseModel):
    email: EmailStr
