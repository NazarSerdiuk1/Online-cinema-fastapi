from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from decimal import Decimal
from uuid import UUID

from db.models import OrderStatus

class MovieBaseSchema(BaseModel):
    id: UUID
    name: str
    year: int
    price: float

    class Config:
        from_attributes = True


class MovieCreateSchema(BaseModel):
    name: str
    year: int
    time: int
    imdb: float
    votes: int
    description: str
    price: float
    certification_id: int

    genre_ids: Optional[List[int]] = []
    director_ids: Optional[List[int]] = []
    star_ids: Optional[List[int]] = []

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