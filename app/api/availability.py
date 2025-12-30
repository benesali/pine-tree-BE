from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, joinedload

from app.db.session import get_db
from app.models.availability import Availability
from app.schemas.availability import AvailabilityDay

router = APIRouter(tags=["availability"])


@router.get(
    "/{apartment_id}/availability",
    response_model=list[AvailabilityDay],
)
def get_availability(
    apartment_id: int,
    from_date: date = Query(..., alias="from"),
    to_date: date = Query(..., alias="to"),
    db: Session = Depends(get_db),
):
    """Retrieve availability records for an apartment within a date range.

    Args:
        apartment_id: ID of the apartment to query availability for.
        from_date: Start date of the requested range (inclusive).
        to_date: End date of the requested range (inclusive).
        db: Database session provided by the `get_db` dependency.

    Returns:
        list[Availability]: A list of `Availability` rows that match the range.
    """

    records = (
        db.query(Availability)
        .join(Availability.reservation)
        .options(joinedload(Availability.reservation))
        .filter(
            Availability.apartment_id == apartment_id,
            Availability.date >= from_date,
            Availability.date <= to_date,
        )
        .all()
    )

    return [
        {
            "date": av.date,
            "status": av.reservation.status,
            "reservation_id": av.reservation.id,
        }
        for av in records
    ]
