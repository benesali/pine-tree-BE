from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.general_dependency import get_db
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
    records = (
        db.query(Availability)
        .filter(
            Availability.apartment_id == apartment_id,
            Availability.date >= from_date,
            Availability.date <= to_date,
        )
        .all()
    )

    # FastAPI + Pydantic:
    # - vezme SQLAlchemy objekty
    # - vytáhne jen pole definované ve schema
    return records
