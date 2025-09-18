from dataclasses import dataclass
from sqlalchemy import Integer, String, Boolean, Float
from sqlalchemy.orm import Mapped, mapped_column
from flaskr.database import db

@dataclass
class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(20))
    password: Mapped[str] = mapped_column(String(20), nullable=False)
    isAdmin: Mapped[bool] = mapped_column(Boolean)

    def to_dict(self):
        return {
            'id': str(self.id),
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'isAdmin': self.isAdmin
        }

@dataclass
class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    author: Mapped[str] = mapped_column(String(50), nullable=False)
    publisher: Mapped[str | None] = mapped_column(String(50))
    price: Mapped[float] = mapped_column(Float, nullable=False)
    discount: Mapped[int | None] = mapped_column(Integer)
    imageUrl: Mapped[str | None] = mapped_column(String(20))

@dataclass
class CartItem(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    userId: Mapped[int] = mapped_column(Integer, nullable=False)
    productId: Mapped[int] = mapped_column(Integer, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)