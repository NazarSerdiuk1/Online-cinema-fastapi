from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import UserModel


def get_current_user(db: Session = Depends(get_db)) -> UserModel:
    user = db.query(UserModel).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user
