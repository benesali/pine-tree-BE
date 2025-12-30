# app/models/reservation.py
from datetime import date
from enum import Enum

from sqlalchemy import Enum as SAEnum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class ReservationStatus(str, Enum):
    RESERVED = "reserved"  # payment waiting
    BOOKED = "booked"  # paid
    BLOCKED = "blocked"  # not available


class Reservation(Base):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(primary_key=True)

    apartment_id: Mapped[int] = mapped_column(
        ForeignKey("apartments.id"),
        index=True,
        nullable=False,
    )

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id"),
        index=True,
        nullable=False,
    )

    date_from: Mapped[date]
    date_to: Mapped[date]

    status: Mapped[ReservationStatus] = mapped_column(
        SAEnum(ReservationStatus),
        index=True,
        nullable=False,
    )

    note: Mapped[str | None] = mapped_column(nullable=True)

    # 🔹 relationships
    apartment = relationship(
        "Apartment",
        back_populates="reservations",
    )

    customer = relationship("Customer")

    availability = relationship(
        "Availability",
        back_populates="reservation",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"<Reservation id={self.id} "
            f"apartment_id={self.apartment_id} "
            f"{self.date_from}→{self.date_to} "
            f"status={self.status}>"
        )
