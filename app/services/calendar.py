# Calendar service for managing availability ranges for admins

from datetime import date, timedelta
from sqlalchemy.orm import Session
from app.models.availability import Availability, AvailabilityStatus

class CalendarService:
    def __init__(self, db: Session):
        self.db = db

    def _date_range(self, start: date, end: date):
        current = start
        while current <= end:
            yield current
            current += timedelta(days=1)

    def set_range(
        self,
        apartment_id: int,
        date_from: date,
        date_to: date,
        status: AvailabilityStatus,
        note: str | None = None,
    ):
        for day in self._date_range(date_from, date_to):
            existing = (
                self.db.query(Availability)
                .filter_by(apartment_id=apartment_id, date=day)
                .first()
            )

            # booked se NESMÍ přepsat
            if existing and existing.status == AvailabilityStatus.booked and status != AvailabilityStatus.booked:
                raise ValueError(f"Date {day} is already booked")

            if not existing:
                self.db.add(
                    Availability(
                        apartment_id=apartment_id,
                        date=day,
                        status=status,
                        note=note,
                    )
                )
            else:
                existing.status = status
                existing.note = note

        self.db.commit()

    def clear_range(self, apartment_id: int, date_from: date, date_to: date):
        (
            self.db.query(Availability)
            .filter(
                Availability.apartment_id == apartment_id,
                Availability.date >= date_from,
                Availability.date <= date_to,
            )
            .delete(synchronize_session=False)
        )
        self.db.commit()
