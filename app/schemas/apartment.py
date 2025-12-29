"""Pydantic schemas for apartment responses."""

from pydantic import BaseModel


class ApartmentListItem(BaseModel):
    """Minimal apartment representation for lists."""

    id: int
    name: str
    location: str


class ApartmentDetail(ApartmentListItem):
    """Detailed apartment representation."""

    description: str | None
