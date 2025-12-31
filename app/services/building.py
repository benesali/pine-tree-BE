from sqlalchemy.orm import Session, joinedload

from app.models.building import Building
from app.schemas.building import (
    ApartmentInBuilding,
    BuildingCard,
    BuildingDetail,
)


class BuildingService:
    def __init__(self, db: Session):
        self.db = db

    def list_buildings(self) -> list[BuildingCard]:
        buildings = self.db.query(Building).filter(Building.is_active).all()

        result = []
        for b in buildings:
            apartments = b.apartments

            guests = [a.guests for a in apartments if a.is_active]
            active_apartments = [a for a in b.apartments if a.is_active]
            prices = [120.0] * len(apartments)  # TODO pricing

            result.append(
                BuildingCard(
                    id=b.id,
                    slug=b.slug,
                    name=b.name,
                    location=b.location,
                    heroImage="/images/house/hero.jpg",
                    previewImages=[
                        "/images/apartments/a/living.jpg",
                        "/images/apartments/b/bedroom.jpg",
                        "/images/apartments/c/terrace.jpg",
                    ],
                    apartmentsCount=len(active_apartments),
                    minGuests=min(guests) if guests else 0,
                    maxGuests=max(guests) if guests else 0,
                    priceFrom=min(prices) if prices else 0,
                    availableApartments=len(apartments),  # TODO availability
                )
            )

        return result

    def get_building_detail(self, slug: str) -> BuildingDetail | None:
        building = (
            self.db.query(Building)
            .options(joinedload(Building.apartments))
            .filter(Building.slug == slug, Building.is_active)
            .first()
        )
        if not building:
            return None

        apartments = [
            ApartmentInBuilding(
                id=a.id,
                slug=a.slug,
                name=a.name,
                guests=a.guests,
                bedrooms=a.bedrooms,
                bathrooms=a.bathrooms,
                priceFrom=120.0,
                available=True,
            )
            for a in building.apartments
            if a.is_active
        ]

        return BuildingDetail(
            id=building.id,
            slug=building.slug,
            name=building.name,
            location=building.location,
            description=building.description,
            images=[
                "/images/house/hero.jpg",
                "/images/house/terrace.jpg",
            ],
            apartments=apartments,
        )
