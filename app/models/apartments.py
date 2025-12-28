# app/models/apartment.py
# model for Apartment entity    
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Apartment(Base):
    __tablename__ = "apartments"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    location: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None]
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, onupdate=datetime.utcnow)

    availability = relationship("Availability", back_populates="apartment")
    reviews = relationship("Review", back_populates="apartment")

    amenities = relationship(
        "Amenity",
        secondary="apartment_amenities",
        lazy="joined"
    )
    services = relationship(
        "Service",
        secondary="apartment_services",
        lazy="joined"
    )
