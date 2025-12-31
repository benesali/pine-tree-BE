from pydantic import BaseModel


class BuildingCard(BaseModel):
    id: int
    slug: str
    name: str
    location: str

    heroImage: str
    previewImages: list[str]

    apartmentsCount: int
    minGuests: int
    maxGuests: int

    priceFrom: float
    availableApartments: int

    class Config:
        from_attributes = True


class ApartmentInBuilding(BaseModel):
    id: int
    slug: str
    name: str
    guests: int
    bedrooms: int
    bathrooms: int
    priceFrom: float
    available: bool


class BuildingDetail(BaseModel):
    id: int
    slug: str
    name: str
    location: str
    description: str | None

    images: list[str]
    apartments: list[ApartmentInBuilding]
