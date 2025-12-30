import enum
from datetime import date

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class AvailabilityStatus(enum.Enum):
    blocked = "blocked"  # unavailable
    reserved = "reserved"  # resrerved, payment pending
    booked = "booked"  # booked, payment completed


class Availability(Base):
    __tablename__ = "availability"

    id: Mapped[int] = mapped_column(primary_key=True)

    apartment_id: Mapped[int] = mapped_column(
        ForeignKey("apartments.id"),
        index=True,
        nullable=False,
    )

    reservation_id: Mapped[int] = mapped_column(
        ForeignKey("reservations.id"),
        index=True,
        nullable=False,
    )

    date: Mapped[date]

    is_available: Mapped[bool] = mapped_column(default=False)

    apartment = relationship(
        "Apartment",
        back_populates="availability",
    )

    reservation = relationship(
        "Reservation",
        back_populates="availability",
    )
