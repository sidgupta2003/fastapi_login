from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import SessionLocal
from .auth import get_current_user

router = APIRouter(prefix="/protected", tags=["protected"])

@router.get("/users/me", response_model=schemas.UserOut)
def read_users_me(current_user: schemas.UserOut = Depends(get_current_user)):
    return current_user