# app/models/customer.py
# model for Customer entity


from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str]
    email2: Mapped[str | None]
    phone: Mapped[str | None]
    phone2: Mapped[str | None]
    adults: Mapped[int]
    children_ages: Mapped[list[int]] = mapped_column(JSON, nullable=True)
    extra_bed: Mapped[bool]
    note: Mapped[str | None] = mapped_column(nullable=True)
    dogs: Mapped[int]  # number of dogs
