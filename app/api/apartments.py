from fastapi import APIRouter

from app.schemas.apartment import ApartmentListItem

router = APIRouter(tags=["apartments"])


@router.get(
    "/",
    response_model=list[ApartmentListItem],
)
def list_apartments():
    return [
        {
            "id": 1,
            "name": "Pine Apartment",
            "location": "Croatia",
        }
    ]
