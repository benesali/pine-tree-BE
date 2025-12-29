# app/models/availability.py
# model for Availability entity
import enum
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class AvailabilityStatus(enum.Enum):
    blocked = "blocked"  # unavailable
    reserved = "reserved"  # resrerved, payment pending
    booked = "booked"  # booked, payment completed


class Availability(Base):
    """Single-day availability record for an apartment."""

    __tablename__ = "availability"
    __table_args__ = (
        UniqueConstraint("apartment_id", "date", name="uq_apartment_date"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    apartment_id: Mapped[int] = mapped_column(ForeignKey("apartments.id"))
    date: Mapped[date] = mapped_column(Date)
    status: Mapped[AvailabilityStatus] = mapped_column(Enum(AvailabilityStatus))
    # not public
    reservation_id: Mapped[int | None] = mapped_column(
        ForeignKey("reservations.id"), nullable=True
    )
    note: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    apartment = relationship("Apartment", back_populates="availability")

    def __repr__(self) -> str:  # pragma: no cover - trivial
        """Return a concise string representation of the Availability row."""
        return f"<Availability id={self.id} apt={self.apartment_id} date={self.date}>"
