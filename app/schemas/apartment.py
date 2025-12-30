from pydantic import BaseModel


class ApartmentBase(BaseModel):
    id: int
    slug: str
    name: str
    description: str | None
    buildingSlug: str
    price: float
    guests: int
    bedrooms: int
    bathrooms: int
    image: str
    images: list[str]
    amenities: list[str]
    available: bool

    class Config:
        from_attributes = True
