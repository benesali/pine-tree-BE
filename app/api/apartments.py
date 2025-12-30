from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.apartment import ApartmentBase
from app.services.apartment import ApartmentService

router = APIRouter()


@router.get("", response_model=list[ApartmentBase])
def list_apartments(db: Session = Depends(get_db)):
    return ApartmentService(db).list_apartments()


@router.get("/{slug}", response_model=ApartmentBase)
def get_apartment(slug: str, db: Session = Depends(get_db)):
    apartment = ApartmentService(db).get_by_slug(slug)
    if not apartment:
        raise HTTPException(status_code=404, detail="Apartment not found")
    return apartment
