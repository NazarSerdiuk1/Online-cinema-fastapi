from sqlalchemy.orm import Session
from fastapi import HTTPException
from db.models import UserModel
from db.schemas import UserCreateSchema

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(UserModel).all()

    def get_by_id(self, user_id: int):
        user = self.db.get(UserModel, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def create(self, data: UserCreateSchema):
        if self.db.query(UserModel).filter(UserModel.email == data.email).first():
            raise HTTPException(status_code=400, detail="Email already exists")

        user = UserModel.create(
            email=data.email,
            raw_password=data.password,
            group_id=data.group_id,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
