from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Building(Base):
    __tablename__ = "buildings"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    name: Mapped[str]
    location: Mapped[str]
    description: Mapped[str | None]
    is_active: Mapped[bool] = mapped_column(default=True)

    apartments = relationship("Apartment", back_populates="building")

    def __repr__(self) -> str:  # pragma: no cover - trivial
        """Return a concise string representation of the Building."""
        return f"<Building id={self.id} slug={self.slug}>"
