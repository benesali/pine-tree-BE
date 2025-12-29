# app/models/review.py
# model for Review entity
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Review(Base):
    """Customer review associated with an apartment."""

    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True)
    apartment_id: Mapped[int | None] = mapped_column(
        ForeignKey("apartments.id"), nullable=True
    )
    author_name: Mapped[str] = mapped_column(String(255))
    text: Mapped[str] = mapped_column(Text)
    is_approved: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    apartment = relationship("Apartment", back_populates="reviews")

    def __repr__(self) -> str:  # pragma: no cover - trivial
        """Return a concise string representation of the Review."""
        return f"<Review id={self.id} apartment_id={self.apartment_id}>"
