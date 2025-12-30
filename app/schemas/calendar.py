from datetime import date

from pydantic import BaseModel, EmailStr, model_validator


# admin calendar management
class CalendarRangeRequest(BaseModel):
    """Request model for admin actions affecting a date range.

    Fields:
        apartment_id: The target apartment identifier.
        date_from: Start date for the action (inclusive).
        date_to: End date for the action (inclusive).
        note: Optional note to attach to created/updated availability rows.
    """

    apartment_id: int
    date_from: date
    date_to: date
    note: str | None = None

    @model_validator(mode="after")
    def validate_range(self):
        """Ensure `date_from` is not after `date_to`.

        Raises:
            ValueError: when `date_from` > `date_to`.
        """
        if self.date_from > self.date_to:
            raise ValueError("date_from must be <= date_to")
        return self


class CalendarActionResponse(BaseModel):
    status: str


class CustomerInput(BaseModel):
    name: str
    email: EmailStr
    email2: EmailStr | None = None
    phone: str | None = None
    phone2: str | None = None
    adults: int
    children_ages: list[int] | None = None
    extra_bed: bool
    note: str | None = None
    dogs: int


class CalendarReserveRequest(BaseModel):
    apartment_id: int
    date_from: date
    date_to: date
    customer: CustomerInput
