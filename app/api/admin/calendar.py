from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.security_dependency import admin_required
from app.db.session import get_db
from app.models.availability import AvailabilityStatus
from app.schemas.calendar import CalendarActionResponse, CalendarRangeRequest
from app.services.calendar import CalendarService

router = APIRouter(prefix="/admin/calendar", tags=["admin-calendar"])


@router.post("/block", response_model=CalendarActionResponse)
def block_range(
    data: CalendarRangeRequest,
    _: str = Depends(admin_required),
    db: Session = Depends(get_db),
):
    """Block a date range for the specified apartment.

    Args:
        data: `CalendarRangeRequest` containing `apartment_id`, `date_from`,
            `date_to`, and `note`.
        _: Unused admin id (value returned by `admin_required`).
        db: SQLAlchemy session provided by the `get_db` dependency.

    Returns:
        A dict with the action status (e.g., `{"status": "blocked"}`).

    Raises:
        HTTPException: 409 when the requested range contains an already-booked day.
    """
    try:
        CalendarService(db).set_range(
            data.apartment_id,
            data.date_from,
            data.date_to,
            AvailabilityStatus.blocked,
            data.note,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=409,
            detail=str(e),
        ) from None

    return {"status": "blocked"}
