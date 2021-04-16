from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from api import schemas
from db import models
from db.database import get_db


router = APIRouter()

@router.get("/", response_model=List[schemas.Tag])
def get_tags(db: Session = Depends(get_db)) -> list:
    return db.query(models.Tag).all()
