from fastapi import APIRouter

from app.schemas.apartment import ApartmentListItem

router = APIRouter(tags=["apartments"])


@router.get(
    "/",
    response_model=list[ApartmentListItem],
)
def list_apartments():
    """Return a list of apartments.

    This is currently a placeholder endpoint that returns a static list of
    apartments. In a production implementation this would query the database
    and return paginated results.

    Returns:
        list[dict]: A list of apartment objects matching `ApartmentListItem`.
    """
    return [
        {
            "id": 1,
            "name": "Pine Apartment",
            "location": "Croatia",
        }
    ]
