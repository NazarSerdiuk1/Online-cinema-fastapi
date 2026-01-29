from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from db.database import get_db
from dependencies import get_current_user
from db.models import UserModel
from db.schemas import CartSchema
from db.repositories.cart_repository import CartRepository

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.get("/", response_model=CartSchema)
def get_cart(
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    repo = CartRepository(db)
    return repo.get_or_create(user)

@router.post("/add/{movie_id}", status_code=status.HTTP_201_CREATED)
def add_to_cart(
    movie_id: UUID,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    repo = CartRepository(db)
    repo.add_movie(user, movie_id)
    return {"detail": "Movie added to cart"}

@router.delete("/clear")
def clear_cart(
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    repo = CartRepository(db)
    repo.clear(user)
    return {"detail": "Cart cleared"}
