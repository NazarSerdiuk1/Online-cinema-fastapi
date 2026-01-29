from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from uuid import UUID

from db.models import Cart, CartItem, Movie, UserModel

class CartRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_or_create(self, user: UserModel) -> Cart:
        if not user.cart:
            user.cart = Cart(user_id=user.id)
            self.db.add(user.cart)
            self.db.commit()
            self.db.refresh(user.cart)
        return user.cart

    def add_movie(self, user: UserModel, movie_id: UUID):
        cart = self.get_or_create(user)
        movie = self.db.get(Movie, movie_id)
        if not movie:
            raise NoResultFound("Movie not found")

        exists = (
            self.db.query(CartItem)
            .filter_by(cart_id=cart.id, movie_id=movie_id)
            .first()
        )
        if exists:
            raise ValueError("Movie already in cart")

        item = CartItem(cart_id=cart.id, movie_id=movie_id)
        self.db.add(item)
        self.db.commit()

    def clear(self, user: UserModel):
        if not user.cart:
            return
        user.cart.items.clear()
        self.db.commit()
