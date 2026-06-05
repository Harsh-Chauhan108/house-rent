from fastapi import APIRouter, Depends, HTTPException
import models
import schemas
from database import SessionLocal
import utils
router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)
from utils.hashing import (
    hash_password,
    verify_password
)




def register(
    user: schemas.RegisterSchema,
    db: Session = Depends(get_db)
):
    existing_user = db.query(models.User).filter(
    models.User.email == user.email
    ).first()
    if existing_user:
        raise HTTPException(400, "Email already exists")
    hashed_password = hash_password(user.password)
    new_user = models.User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        role=user.role
    )
    db.add(new_user)
    db.commit()
    return {
    "message": "User Registered Successfully"
    }