from datetime import date
from pydantic import BaseModel
from app.models.availability import AvailabilityStatus

# FE calendar
class AvailabilityDay(BaseModel):
    date: date
    status: AvailabilityStatus
