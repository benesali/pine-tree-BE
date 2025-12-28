# app/models/reservation.py
# model for Reservation entity
class Reservation(Base):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(primary_key=True)
    apartment_id: Mapped[int] = mapped_column(ForeignKey("apartments.id"))
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    date_from: Mapped[date]
    date_to: Mapped[date]
    status: Mapped[ReservationStatus]
