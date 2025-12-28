# app/models/amenity.py
# model for Amenity entity
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Amenity(Base):
    __tablename__ = "amenities"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(50), unique=True)
    label: Mapped[str] = mapped_column(String(255))
    icon: Mapped[str | None]
