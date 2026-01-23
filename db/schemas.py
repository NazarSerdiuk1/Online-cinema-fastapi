from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from typing import List, Optional
from decimal import Decimal
from uuid import UUID

from db.models import OrderStatus, UserGroupEnum, GenderEnum

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

class UserSchema(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime
    group_id: int

    class Config:
        from_attributes = True

class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str
    group_id: int

class UserProfileCreateSchema(BaseModel):
    user_id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar: Optional[str] = None
    gender: Optional[GenderEnum] = None
    date_of_birth: Optional[date] = None
    info: Optional[str] = None

class UserProfileSchema(BaseModel):
    id: int
    first_name: Optional[str]
    last_name: Optional[str]
    avatar: Optional[str]
    gender: Optional[GenderEnum]
    date_of_birth: Optional[date]
    info: Optional[str]

    class Config:
        from_attributes = True