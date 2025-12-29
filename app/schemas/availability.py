"""Schemas used to serialize availability data to the front-end."""

from datetime import date

from pydantic import BaseModel

from app.models.availability import AvailabilityStatus


class AvailabilityDay(BaseModel):
    """A single day availability payload for the calendar UI."""

    date: date
    status: AvailabilityStatus
