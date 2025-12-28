from datetime import date
from pydantic import BaseModel, model_validator

# admin calendar management
class CalendarRangeRequest(BaseModel):
    apartment_id: int
    date_from: date
    date_to: date
    note: str | None = None

    @model_validator(mode="after")
    def validate_range(self):
        if self.date_from > self.date_to:
            raise ValueError("date_from must be <= date_to")
        return self

class CalendarActionResponse(BaseModel):
    status: str
