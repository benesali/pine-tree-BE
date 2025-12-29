# app/models/apartment_amenity.py
# M:N association table for Apartment and Amenity entities
from sqlalchemy import Column, ForeignKey, Integer, Table

from app.db.base import Base

apartment_amenities = Table(
    "apartment_amenities",
    Base.metadata,
    Column("apartment_id", Integer, ForeignKey("apartments.id"), primary_key=True),
    Column("amenity_id", Integer, ForeignKey("amenities.id"), primary_key=True),
)
