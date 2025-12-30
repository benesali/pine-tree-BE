from datetime import date
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class ApartmentPricePeriod(Base):
    __tablename__ = "apartment_price_periods"

    id: Mapped[int] = mapped_column(primary_key=True)

    apartment_id: Mapped[int] = mapped_column(
        ForeignKey("apartments.id"),
        index=True,
        nullable=False,
    )

    date_from: Mapped[date]
    date_to: Mapped[date]

    price_per_night: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    label: Mapped[str | None]  # "High season", "Low season"

    apartment = relationship("Apartment", back_populates="price_periods")
