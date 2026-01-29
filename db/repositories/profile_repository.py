from sqlalchemy.orm import Session
from fastapi import HTTPException
from db.models import UserProfileModel, UserModel
from db.schemas import UserProfileCreateSchema

class UserProfileRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_user_id(self, user_id: int):
        profile = self.db.query(UserProfileModel).filter(UserProfileModel.user_id == user_id).first()
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        return profile

    def create(self, data: UserProfileCreateSchema):
        user = self.db.get(UserModel, data.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user.profile:
            raise HTTPException(status_code=400, detail="Profile already exists")

        profile = UserProfileModel(**data.model_dump())
        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)
        return profile
