from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.models.availability import Availability
from app.models.customer import Customer
from app.models.reservation import Reservation, ReservationStatus

SYSTEM_BLOCKED_EMAIL = "system@blocked.local"


def get_or_create_blocked_customer(db: Session) -> Customer:
    """
    Return the system customer used for BLOCKED reservations.
    Creates the customer if it does not exist yet.
    """
    customer = db.query(Customer).filter(Customer.email == SYSTEM_BLOCKED_EMAIL).first()

    if customer:
        return customer

    customer = Customer(
        name="BLOCKED",
        email=SYSTEM_BLOCKED_EMAIL,
        adults=0,
        children_ages=[],
        extra_bed=False,
    )
    db.add(customer)
    db.flush()

    return customer


def get_or_create_customer(db, data):
    customer = db.query(Customer).filter(Customer.email == data.email).first()

    if customer:
        return customer

    customer = Customer(
        name=data.name,
        email=data.email,
        email2=data.email2,
        phone=data.phone,
        phone2=data.phone2,
        adults=data.adults,
        children_ages=data.children_ages,
        extra_bed=data.extra_bed,
        note=data.note,
        dogs=data.dogs,
    )

    db.add(customer)
    db.flush()
    return customer


class CalendarService:
    def __init__(self, db: Session):
        self.db = db

    def set_range(
        self,
        apartment_id: int,
        date_from: date,
        date_to: date,
        status: ReservationStatus,
        note: str | None = None,
        customer_data: dict | None = None,
    ) -> Reservation:
        """
        Create a reservation for the given date range and generate
        daily availability records.

        Rules:
        - Reservation is the source of truth for status
        - Availability is purely technical (one row per day)
        - BOOKED days cannot be overridden
        """

        if date_from > date_to:
            raise ValueError("date_from must be before or equal to date_to")

        # Check for conflicts with already booked days
        conflict = (
            self.db.query(Availability)
            .join(Availability.reservation)
            .filter(
                Availability.apartment_id == apartment_id,
                Availability.date >= date_from,
                Availability.date <= date_to,
                Reservation.status == ReservationStatus.BOOKED,
            )
            .first()
        )

        if conflict:
            raise ValueError("Date range contains already booked days")

        # Select customer depending on reservation type
        if status == ReservationStatus.BLOCKED:
            customer = get_or_create_blocked_customer(self.db)

        elif status in (ReservationStatus.RESERVED, ReservationStatus.BOOKED):
            if not customer_data:
                raise ValueError("Customer data required")
            customer = get_or_create_customer(self.db, customer_data)

        else:
            raise ValueError("Unsupported reservation status")
        # Create reservation
        reservation = Reservation(
            apartment_id=apartment_id,
            customer_id=customer.id,
            date_from=date_from,
            date_to=date_to,
            status=status,
        )

        self.db.add(reservation)
        self.db.flush()

        # Create availability rows per day
        current = date_from
        while current <= date_to:
            self.db.add(
                Availability(
                    apartment_id=apartment_id,
                    reservation_id=reservation.id,
                    date=current,
                    is_available=False,
                )
            )
            current += timedelta(days=1)

        self.db.commit()
        return reservation

    def clear_range(
        self,
        apartment_id: int,
        date_from: date,
        date_to: date,
    ) -> None:
        """
        Remove all reservations that intersect the given date range.
        Availability rows are removed automatically via cascade.
        """

        reservations = (
            self.db.query(Reservation)
            .join(Reservation.availability)
            .filter(
                Reservation.apartment_id == apartment_id,
                Availability.date >= date_from,
                Availability.date <= date_to,
            )
            .distinct()
            .all()
        )

        for reservation in reservations:
            self.db.delete(reservation)

        self.db.commit()
