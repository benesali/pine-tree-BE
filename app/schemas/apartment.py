from pydantic import BaseModel

class ApartmentListItem(BaseModel):
    id: int
    name: str
    location: str

class ApartmentDetail(ApartmentListItem):
    description: str | None
