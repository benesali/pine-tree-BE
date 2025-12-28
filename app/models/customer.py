# app/models/customer.py
# model for Customer entity 
class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str]
    adults: Mapped[int]
    children_count: Mapped[int]
    children_ages: Mapped[list[int] | None]
    extra_bed: Mapped[bool]
