from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import get_current_user
from db.database import get_db
from db.repositories.order_repository import OrderRepository
from db.schemas import OrderSchema
from db.models import UserModel

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderSchema)
def create_order(
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    repo = OrderRepository(db)
    return repo.create(user)

@router.get("/", response_model=list[OrderSchema])
def get_my_orders(
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    repo = OrderRepository(db)
    return repo.get_by_user(user)

@router.post("/{order_id}/cancel")
def cancel_order(
    order_id: int,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user),
):
    repo = OrderRepository(db)
    return repo.cancel(order_id, user)
