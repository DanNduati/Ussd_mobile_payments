from typing import List
from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.orm import Session
from .. import schemas, models
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Add a user
    """
    if not(db.query(models.User).filter(
            models.User.phonenumber == user.phonenumber).first()):
        new_user = models.User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail="User already exists!")


@router.get("/{phone_number}", response_model=schemas.UserResponse)
async def get_users(phone_number: int, db: Session = Depends(get_db)):
    """
    Get user by phone number
    """
    user = db.query(models.User).filter(
        models.User.phonenumber == phone_number).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exists!")
    return user
