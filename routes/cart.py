from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.database import get_db
from dependencies import get_current_user
from db.models import Cart, CartItem, Movie, UserModel
from db.schemas import CartSchema

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.get("/", response_model=CartSchema)
def get_cart(
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    if not user.cart:
        user.cart = Cart(user_id=user.id)
        db.add(user.cart)
        db.commit()
        db.refresh(user.cart)

    return user.cart

@router.post("/add/{movie_id}", status_code=status.HTTP_201_CREATED)
def add_to_cart(
    movie_id: int,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    if not user.cart:
        user.cart = Cart(user_id=user.id)
        db.add(user.cart)
        db.commit()

    movie = db.get(Movie, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    exists = (
        db.query(CartItem)
        .filter_by(cart_id=user.cart.id, movie_id=movie_id)
        .first()
    )
    if exists:
        raise HTTPException(status_code=400, detail="Movie already in cart")

    item = CartItem(cart_id=user.cart.id, movie_id=movie_id)
    db.add(item)
    db.commit()

    return {"detail": "Movie added to cart"}

@router.delete("/clear")
def clear_cart(
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    if not user.cart:
        return {"detail": "Cart already empty"}

    user.cart.items.clear()
    db.commit()
    return {"detail": "Cart cleared"}