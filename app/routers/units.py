from typing import List
from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.orm import Session
from .. import schemas, models
from ..database import get_db

router = APIRouter(
    prefix="/units",
    tags=["Units"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UnitBase)
async def create_unit(unit: schemas.UnitCreate, db: Session = Depends(get_db)):
    """
    Add a unit
    """
    new_unit = models.Unit(**unit.dict())
    db.add(new_unit)
    db.commit()
    db.refresh(new_unit)
    return new_unit


@router.get("/{unit_id}", response_model=schemas.UnitBase)
async def get_users(unit_id: int, db: Session = Depends(get_db)):
    """
    Get unit by id
    """
    unit = db.query(models.Unit).filter(
        models.Unit.id == unit_id).first()
    if not unit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Unit doesn't exists!")
    return unit
