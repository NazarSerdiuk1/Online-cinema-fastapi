from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import UserModel
from db.schemas import (
    UserCreateSchema, UserSchema
)

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def create_user(
    data: UserCreateSchema,
    db: Session = Depends(get_db),
):
    if db.query(UserModel).filter(UserModel.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    user = UserModel.create(
        email=data.email,
        raw_password=data.password,
        group_id=data.group_id,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

@router.get("/", response_model=list[UserSchema])
def list_users(db: Session = Depends(get_db)):
    return db.query(UserModel).all()


@router.get("/{user_id}", response_model=UserSchema)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(UserModel, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user