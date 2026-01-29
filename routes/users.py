from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_db
from db.repositories.user_repository import UserRepository
from db.schemas import UserCreateSchema, UserSchema

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserSchema)
def create_user(
    data: UserCreateSchema,
    db: Session = Depends(get_db),
):
    repo = UserRepository(db)
    return repo.create(data)

@router.get("/", response_model=list[UserSchema])
def list_users(db: Session = Depends(get_db)):
    repo = UserRepository(db)
    return repo.get_all()

@router.get("/{user_id}", response_model=UserSchema)
def get_user(user_id: int, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    return repo.get_by_id(user_id)
