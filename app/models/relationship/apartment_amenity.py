# app/models/apartment_amenity.py
# M:N association table for Apartment and Amenity entities
from sqlalchemy import ForeignKey, Table
from app.db.base import Base

apartment_amenities = Table(
    "apartment_amenities",
    Base.metadata,
    ForeignKey("apartments.id"),
    ForeignKey("amenities.id"),
)
