from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import UserProfileModel, UserModel
from db.schemas import (
    UserProfileCreateSchema, UserProfileSchema
)

router = APIRouter(prefix="/profiles", tags=["Profiles"])

@router.post("/", response_model=UserProfileSchema)
def create_profile(
    data: UserProfileCreateSchema,
    db: Session = Depends(get_db),
):
    user = db.get(UserModel, data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.profile:
        raise HTTPException(status_code=400, detail="Profile already exists")

    profile = UserProfileModel(**data.model_dump())

    db.add(profile)
    db.commit()
    db.refresh(profile)

    return profile

@router.get("/{user_id}", response_model=UserProfileSchema)
def get_profile(user_id: int, db: Session = Depends(get_db)):
    profile = (
        db.query(UserProfileModel)
        .filter(UserProfileModel.user_id == user_id)
        .first()
    )
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

