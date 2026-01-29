from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_db
from db.repositories.profile_repository import UserProfileRepository
from db.schemas import UserProfileCreateSchema, UserProfileSchema

router = APIRouter(prefix="/profiles", tags=["Profiles"])

@router.post("/", response_model=UserProfileSchema)
def create_profile(
    data: UserProfileCreateSchema,
    db: Session = Depends(get_db),
):
    repo = UserProfileRepository(db)
    return repo.create(data)

@router.get("/{user_id}", response_model=UserProfileSchema)
def get_profile(user_id: int, db: Session = Depends(get_db)):
    repo = UserProfileRepository(db)
    return repo.get_by_user_id(user_id)
