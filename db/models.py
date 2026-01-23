import enum
from datetime import datetime, date, timedelta, timezone
from typing import List, Optional
import uuid as uuid_pkg
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy import (
    ForeignKey,
    String,
    Boolean,
    DateTime,
    Enum,
    Integer,
    func,
    Text,
    Date,
    UniqueConstraint,
    Table,
    Column,
    Numeric,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
    validates
)

from db.database import Base
from db.validators import accounts as validators
from db.security.passwords import hash_password, verify_password
from db.security.utils import generate_secure_token


class UserGroupEnum(str, enum.Enum):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"

class GenderEnum(str, enum.Enum):
    MAN = "man"
    WOMAN = "woman"

class UserGroupModel(Base):
    __tablename__ = "user_groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[UserGroupEnum] = mapped_column(Enum(UserGroupEnum), nullable=False, unique=True)
    users: Mapped[List["UserModel"]] = relationship("UserModel", back_populates="group")

    def __repr__(self):
        return f"<UserGroupModel(id={self.id}, name={self.name})>"
    

class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column("hashed_password", String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
    group_id: Mapped[int] = mapped_column(ForeignKey("user_groups.id", ondelete="CASCADE"), nullable=False)
    
    activation_token: Mapped[Optional["ActivationTokenModel"]] = relationship(
        "ActivationTokenModel",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    password_reset_token: Mapped[Optional["PasswordResetTokenModel"]] = relationship(
        "PasswordResetTokenModel",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    refresh_tokens: Mapped[List["RefreshTokenModel"]] = relationship(
        "RefreshTokenModel",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    profile: Mapped[Optional["UserProfileModel"]] = relationship(
        "UserProfileModel",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
    cart: Mapped["Cart"] = relationship(
    "Cart",
    back_populates="user",
    uselist=False,
    )

    orders: Mapped[list["Order"]] = relationship(
    "Order",
    back_populates="user",
    )

    @property
    def password(self) -> None:
        raise AttributeError("Password is write-only. Use the setter to set the password.")
    
    @password.setter
    def password(self, raw_password: str) -> None:
        validators.validate_password_strength(raw_password)
        self._hashed_password = hash_password(raw_password)
    
    def verify_password(self, raw_password: str) -> bool:
        return verify_password(raw_password, self._hashed_password)
    
    @validates("email")
    def validate_email(self, key, value):
        return validators.validate_email(value.lower())

    def __repr__(self):
        return f"<UserModel(id={self.id}, email={self.email}, is_active={self.is_active})>"

    def has_group(self, group_name: UserGroupEnum) -> bool:
        return self.group.name == group_name
    
    @classmethod
    def create(cls, email: str, raw_password: str, group_id: int | Mapped[int]) -> "UserModel":

        user = cls(email=email, group_id=group_id)
        user.password = raw_password
        return user
    
class UserProfileModel(Base):
    __tablename__ = "user_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(100))
    last_name: Mapped[Optional[str]] = mapped_column(String(100))
    avatar: Mapped[Optional[str]] = mapped_column(String(255))
    gender: Mapped[Optional[GenderEnum]] = mapped_column(Enum(GenderEnum))    
    date_of_birth: Mapped[Optional[date]] = mapped_column(Date)
    info: Mapped[Optional[str]] = mapped_column(Text)
    user: Mapped[UserModel] = relationship("UserModel", back_populates="profile")

    __table_args__ = (UniqueConstraint("user_id"),)

    def __repr__(self):
        return (
            f"<UserProfileModel(id={self.id}, first_name={self.first_name}, last_name={self.last_name}, "
            f"gender={self.gender}, date_of_birth={self.date_of_birth})>"
        )

class TokenBaseModel(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    token: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        nullable=False,
        default=generate_secure_token
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc) + timedelta(days=1)
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

class ActivationTokenModel(TokenBaseModel):
    __tablename__ = "activation_tokens"
    user: Mapped[UserModel] = relationship("UserModel", back_populates="activation_token")
    __table_args__ = (UniqueConstraint("user_id"),)
    
    def __repr__(self):
        return f"<ActivationTokenModel(id={self.id}, token={self.token}, expires_at={self.expires_at})>"

class PasswordResetTokenModel(TokenBaseModel):
    __tablename__ = "password_reset_tokens"
    user: Mapped[UserModel] = relationship("UserModel", back_populates="password_reset_token")
    
    __table_args__ = (UniqueConstraint("user_id"),)
    
    def __repr__(self):
        return f"<PasswordResetTokenModel(id={self.id}, token={self.token}, expires_at={self.expires_at})>"

class RefreshTokenModel(TokenBaseModel):
    __tablename__ = "refresh_tokens"
    user: Mapped[UserModel] = relationship("UserModel", back_populates="refresh_tokens")
    token: Mapped[str] = mapped_column(
        String(512),
        unique=True,
        nullable=False,
        default=generate_secure_token
    )

    @classmethod
    def create(cls, user_id: int | Mapped[int], days_valid: int, token: str) -> "RefreshTokenModel":
        expires_at = datetime.now(timezone.utc) + timedelta(days=days_valid)
        return cls(user_id=user_id, expires_at=expires_at, token=token)
    
    def __repr__(self):
        return f"<RefreshTokenModel(id={self.id}, token={self.token}, expires_at={self.expires_at})>"
    
movie_genres = Table(
    "movie_genres",
    Base.metadata,
    Column("movie_id", ForeignKey("movies.id"), primary_key=True),
    Column("genre_id", ForeignKey("genres.id"), primary_key=True),
)

movie_directors = Table(
    "movie_directors",
    Base.metadata,
    Column("movie_id", ForeignKey("movies.id"), primary_key=True),
    Column("director_id", ForeignKey("directors.id"), primary_key=True),
)

movie_stars = Table(
    "movie_stars",
    Base.metadata,
    Column("movie_id", ForeignKey("movies.id"), primary_key=True),
    Column("star_id", ForeignKey("stars.id"), primary_key=True),
)




class GenreModel(Base):
        __tablename__ = "genres"

        id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
        name: Mapped[str] = mapped_column(unique=True, nullable=False)
        
        movies: Mapped[list["Movie"]] = relationship(
        secondary=movie_genres, back_populates="genres"
    )
    
class StarModel(Base):
        __tablename__ = "stars"

        id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
        name: Mapped[str] = mapped_column(unique=True, nullable=False)
        movies: Mapped[list["Movie"]] = relationship(
        secondary=movie_stars, back_populates="stars"
    )

class DirectorModel(Base):
        __tablename__ = "directors"

        id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
        name: Mapped[str] = mapped_column(unique=True, nullable=False)
        movies: Mapped[list["Movie"]] = relationship(
        secondary=movie_directors, back_populates="directors"
    )
 
class CertificationModel(Base):
        __tablename__ = "certifications"

        id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
        name: Mapped[str] = mapped_column(unique=True, nullable=False)       
        movies: Mapped[list["Movie"]] = relationship(back_populates="certification")

class Movie(Base):
    __tablename__ = "movies"
    __table_args__ = (
        UniqueConstraint("name", "year", "time", name="uq_movie_identity"),
    )
    
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid_pkg.uuid4,
    )

    name: Mapped[str] = mapped_column(nullable=False)
    year: Mapped[int] = mapped_column(nullable=False)
    time: Mapped[int] = mapped_column(nullable=False)

    imdb: Mapped[float] = mapped_column(nullable=False)
    votes: Mapped[int] = mapped_column(nullable=False)

    meta_score: Mapped[float | None]
    gross: Mapped[float | None]

    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2))
    
    certification_id: Mapped[int] = mapped_column(
        ForeignKey("certifications.id"), nullable=False
    )

    certification: Mapped["CertificationModel"] = relationship(back_populates="movies")

    genres: Mapped[list["GenreModel"]] = relationship(
        secondary=movie_genres, back_populates="movies"
    )
    directors: Mapped[list["DirectorModel"]] = relationship(
        secondary=movie_directors, back_populates="movies"
    )
    stars: Mapped[list["StarModel"]] = relationship(
        secondary=movie_stars, back_populates="movies"
    )
    cart_items: Mapped[list["CartItem"]] = relationship("CartItem")

    order_items: Mapped[list["OrderItem"]] = relationship("OrderItem")

class Cart(Base):
    __tablename__ = "carts"

    id: Mapped[int] = mapped_column(primary_key=True)
    
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        unique=True,
    )
    
    user: Mapped["UserModel"] = relationship(
        "UserModel",
        back_populates="cart",
        uselist=False,
    )

    items: Mapped[list["CartItem"]] = relationship(
        "CartItem",
        back_populates="cart",
        cascade="all, delete-orphan",
    )

class CartItem(Base):
    __tablename__ = "cart_items"
    __table_args__ = (
        UniqueConstraint(
            "cart_id",
            "movie_id",
            name="uq_cart_movie",
        ),
    )
    
    id: Mapped[int] = mapped_column(primary_key=True)

    cart_id: Mapped[int] = mapped_column(
        ForeignKey("carts.id"),
        nullable=False,
    )

    movie_id: Mapped[int] = mapped_column(
        ForeignKey("movies.id"),
        nullable=False,
    )
    added_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
    cart: Mapped["Cart"] = relationship(
        "Cart",
        back_populates="items",
    )

    movie: Mapped["Movie"] = relationship("Movie")

class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    CANCELED = "canceled"

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
            ForeignKey("users.id"),
            nullable=False,
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus),
        default=OrderStatus.PENDING,
        nullable=False,
    )
    
    total_amount: Mapped[float | None] = mapped_column(
        Numeric(10, 2)
    )
    user: Mapped["UserModel"] = relationship(
        "UserModel",
        back_populates="orders",
    )
    
    items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
    )
class OrderItem(Base):
    __tablename__ = "order_items"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id"),
        nullable=False,
    )

    movie_id: Mapped[int] = mapped_column(
        ForeignKey("movies.id"),
        nullable=False,
    )

    price_at_order: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    order: Mapped["Order"] = relationship(
        "Order",
        back_populates="items",
    )

    movie: Mapped["Movie"] = relationship("Movie")