from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.security_dependency import admin_required
from app.db.session import get_db
from app.models.reservation import ReservationStatus
from app.schemas.calendar import (
    CalendarActionResponse,
    CalendarRangeRequest,
    CalendarReserveRequest,
)
from app.services.calendar import CalendarService

router = APIRouter()


@router.post("/block", response_model=CalendarActionResponse)
def block_range(
    data: CalendarRangeRequest,
    _: str = Depends(admin_required),
    db: Session = Depends(get_db),
):
    """
    Block a date range for the specified apartment.

    Creates a BLOCKED reservation and generates availability records
    for each day in the range.

    Raises:
        HTTPException(409): If the range contains already booked days.
    """
    try:
        CalendarService(db).set_range(
            apartment_id=data.apartment_id,
            date_from=data.date_from,
            date_to=data.date_to,
            status=ReservationStatus.BLOCKED,
            note=data.note,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=409,
            detail=str(e),
        ) from None

    return {"status": "blocked"}


@router.post("/clear", response_model=CalendarActionResponse)
def clear_range(
    data: CalendarRangeRequest,
    _: str = Depends(admin_required),
    db: Session = Depends(get_db),
):
    """
    Remove all reservations intersecting the given date range.
    """
    CalendarService(db).clear_range(
        apartment_id=data.apartment_id,
        date_from=data.date_from,
        date_to=data.date_to,
    )

    return {"status": "cleared"}


@router.post("/reserve", response_model=CalendarActionResponse)
def reserve_range(
    data: CalendarReserveRequest,
    _: str = Depends(admin_required),
    db: Session = Depends(get_db),
):
    try:
        CalendarService(db).set_range(
            apartment_id=data.apartment_id,
            date_from=data.date_from,
            date_to=data.date_to,
            status=ReservationStatus.RESERVED,
            customer_data=data.customer,
        )
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e)) from None

    return {"status": "reserved"}


@router.post("/book", response_model=CalendarActionResponse)
def book_range(
    data: CalendarReserveRequest,
    _: str = Depends(admin_required),
    db: Session = Depends(get_db),
):
    try:
        CalendarService(db).set_range(
            apartment_id=data.apartment_id,
            date_from=data.date_from,
            date_to=data.date_to,
            status=ReservationStatus.BOOKED,
            customer_data=data.customer,
        )
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e)) from None

    return {"status": "booked"}
