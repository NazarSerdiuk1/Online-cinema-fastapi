from pydantic import BaseModel
from datetime import datetime
from typing import List
from decimal import Decimal
from models import OrderStatus
import uuid


class MovieBaseSchema(BaseModel):
    id: int
    uuid: uuid.UUID
    name: str
    year: int
    price: float

    class Config:
        from_attributes = True

class CartItemSchema(BaseModel):
    id: int
    added_at: datetime
    movie: MovieBaseSchema

    class Config:
        from_attributes = True


class CartSchema(BaseModel):
    id: int
    items: List[CartItemSchema]

    class Config:
        from_attributes = True

class OrderItemSchema(BaseModel):
    id: int
    price_at_order: Decimal
    movie: MovieBaseSchema

    class Config:
        from_attributes = True

class OrderSchema(BaseModel):
    id: int
    created_at: datetime
    status: OrderStatus
    total_amount: Decimal | None
    items: List[OrderItemSchema]

    class Config:
        from_attributes = True