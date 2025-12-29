"""Calendar service for managing availability ranges for admins."""

from collections.abc import Iterator
from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.models.availability import Availability, AvailabilityStatus


class CalendarService:
    """Encapsulate calendar-related operations that modify availability rows.

    The service expects a SQLAlchemy Session object and commits/rolls back
    as part of its operations.
    """

    def __init__(self, db: Session):
        """Initialize the service with a database session.

        Args:
            db: A SQLAlchemy Session used to perform queries and persist changes.
        """
        self.db = db

    def _date_range(self, start: date, end: date) -> Iterator[date]:
        """Yield dates from `start` to `end` (inclusive).

        Args:
            start: The start date (inclusive).
            end: The end date (inclusive).

        Yields:
            date: Each date in the inclusive range.
        """
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
    ) -> None:
        """Set availability `status` for each date in the inclusive range.

        Args:
            apartment_id: Identifier of the apartment.
            date_from: Start date (inclusive).
            date_to: End date (inclusive).
            status: The AvailabilityStatus to set for each date.
            note: Optional note to attach to created/updated availability rows.

        Raises:
            ValueError: When attempting to overwrite an already booked day.

        Returns:
            None
        """
        for day in self._date_range(date_from, date_to):
            existing = (
                self.db.query(Availability)
                .filter_by(apartment_id=apartment_id, date=day)
                .first()
            )

            # Do not overwrite booked days with a non-booked status
            if (
                existing
                and existing.status == AvailabilityStatus.booked
                and status != AvailabilityStatus.booked
            ):
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

    def clear_range(self, apartment_id: int, date_from: date, date_to: date) -> None:
        """Remove availability entries for the given date range.

        Args:
            apartment_id: Identifier of the apartment.
            date_from: Start date (inclusive).
            date_to: End date (inclusive).

        Returns:
            None
        """
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
