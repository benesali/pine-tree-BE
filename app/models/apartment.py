# app/models/apartment.py
from datetime import datetime

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Apartment(Base):
    """Apartment entity representing a rentable unit.

    Stores identifying metadata and defines relationships to reservations,
    availability, reviews and amenities.
    """

    __tablename__ = "apartments"

    id: Mapped[int] = mapped_column(primary_key=True)

    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    location: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None]

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime, onupdate=datetime.utcnow
    )

    # 🔹 Rezervace (business objekt)
    reservations = relationship(
        "Reservation",
        back_populates="apartment",
        cascade="all, delete-orphan",
    )

    # 🔹 Availability (technická tabulka po dnech)
    availability = relationship(
        "Availability",
        back_populates="apartment",
        cascade="all, delete-orphan",
    )

    # Hodnocení
    reviews = relationship(
        "Review",
        back_populates="apartment",
    )

    # Vybavení
    amenities = relationship(
        "Amenity",
        secondary="apartment_amenities",
        lazy="joined",
    )

    # Cenik
    price_periods = relationship(
        "ApartmentPricePeriod",
        back_populates="apartment",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Apartment id={self.id} slug={self.slug!r}>"
