from pydantic import BaseModel
from typing import List, Optional


class UnitBase(BaseModel):
    id: int
    value: int
    user_id: int

    class Config:
        orm_mode = True


class UnitCreate(BaseModel):
    value: int
    user_id: int


class UserBase(BaseModel):
    id: int
    name: str
    phonenumber: int


class UserCreate(BaseModel):
    name: str
    phonenumber: int


class UserResponse(UserBase):
    units: List[UnitBase]

    class Config:
        orm_mode = True


class UssdResponse(BaseModel):
    session_id: str
    service_code: str
    phone_number: str
    text: str
