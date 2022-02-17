from re import L
from pydantic import BaseModel
from typing import List


class UnitBase(BaseModel):
    value: int
    user_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str
    phonenumber: str
    items: List[UnitBase]

    class Config:
        orm_mode = True
