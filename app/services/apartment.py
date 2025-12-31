from sqlalchemy.orm import Session

from app.models.apartment import Apartment
from app.schemas.apartment import ApartmentBase


class ApartmentService:
    def __init__(self, db: Session):
        self.db = db

    def list_apartments(self) -> list[ApartmentBase]:
        apartments = self.db.query(Apartment).filter(Apartment.is_active).all()

        return [self._map_apartment(a) for a in apartments]

    def get_by_slug(self, slug: str) -> ApartmentBase | None:
        apartment = (
            self.db.query(Apartment)
            .filter(Apartment.slug == slug, Apartment.is_active)
            .first()
        )
        if not apartment:
            return None

        return self._map_apartment(apartment)

    def _map_apartment(self, apartment: Apartment) -> ApartmentBase:
        return ApartmentBase(
            id=apartment.id,
            slug=apartment.slug,
            name=apartment.name,
            description=apartment.description,
            buildingSlug=apartment.building.slug,
            price=120.0,  # TODO: pricing logic later
            guests=4,  # TODO: move to DB later
            bedrooms=2,
            bathrooms=1,
            image="/images/default.jpg",
            images=[],
            amenities=[a.label for a in apartment.amenities],
            available=True,
        )
