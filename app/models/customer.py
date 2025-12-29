# app/models/customer.py
# model for Customer entity


from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str]
    adults: Mapped[int]
    children_ages: Mapped[list[int]] = mapped_column(JSON, nullable=True)
    extra_bed: Mapped[bool]
