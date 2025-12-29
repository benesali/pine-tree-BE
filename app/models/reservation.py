from datetime import date
from enum import Enum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ReservationStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"


class Reservation(Base):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(primary_key=True)
    apartment_id: Mapped[int] = mapped_column(ForeignKey("apartments.id"))
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))

    date_from: Mapped[date]
    date_to: Mapped[date]

    status: Mapped[ReservationStatus]
