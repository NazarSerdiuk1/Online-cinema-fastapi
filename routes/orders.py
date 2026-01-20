from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from decimal import Decimal

from db.database import get_db
from dependencies import get_current_user
from db.models import (
    Order,
    OrderItem,
    OrderStatus,
    UserModel,
)
from db.schemas import OrderSchema

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=OrderSchema)
def create_order(
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    if not user.cart or not user.cart.items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    order = Order(user_id=user.id)
    db.add(order)
    db.flush()

    total = Decimal("0.00")

    for item in user.cart.items:
        price = item.movie.price
        total += price

        order_item = OrderItem(
            order_id=order.id,
            movie_id=item.movie_id,
            price_at_order=price,
        )
        db.add(order_item)

    order.total_amount = total
    user.cart.items.clear()

    db.commit()
    db.refresh(order)
    return order

@router.get("/", response_model=list[OrderSchema])
def get_my_orders(
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    return (
        db.query(Order)
        .filter(Order.user_id == user.id)
        .order_by(Order.created_at.desc())
        .all()
    )

@router.post("/{order_id}/cancel")
def cancel_order(
    order_id: int,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    order = db.get(Order, order_id)

    if not order or order.user_id != user.id:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status != OrderStatus.PENDING:
        raise HTTPException(status_code=400, detail="Cannot cancel this order")

    order.status = OrderStatus.CANCELED
    db.commit()

    return {"detail": "Order canceled"}