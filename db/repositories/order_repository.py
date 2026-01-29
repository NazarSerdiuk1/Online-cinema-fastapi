from sqlalchemy.orm import Session
from decimal import Decimal
from fastapi import HTTPException
from db.models import Order, OrderItem, OrderStatus, UserModel

class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_user(self, user: UserModel):
        return self.db.query(Order).filter(Order.user_id == user.id).order_by(Order.created_at.desc()).all()

    def create(self, user: UserModel):
        if not user.cart or not user.cart.items:
            raise HTTPException(status_code=400, detail="Cart is empty")

        order = Order(user_id=user.id)
        self.db.add(order)
        self.db.flush()  # Щоб отримати order.id

        total = Decimal("0.00")
        for item in user.cart.items:
            total += item.movie.price
            self.db.add(OrderItem(order_id=order.id, movie_id=item.movie_id, price_at_order=item.movie.price))

        order.total_amount = total
        user.cart.items.clear()

        self.db.commit()
        self.db.refresh(order)
        return order

    def cancel(self, order_id: int, user: UserModel):
        order = self.db.get(Order, order_id)
        if not order or order.user_id != user.id:
            raise HTTPException(status_code=404, detail="Order not found")
        if order.status != OrderStatus.PENDING:
            raise HTTPException(status_code=400, detail="Cannot cancel this order")

        order.status = OrderStatus.CANCELED
        self.db.commit()
        return order
