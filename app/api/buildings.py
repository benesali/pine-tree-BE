from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.building import BuildingCard, BuildingDetail
from app.services.building import BuildingService

router = APIRouter()


@router.get("", response_model=list[BuildingCard])
def list_buildings(db: Session = Depends(get_db)):
    return BuildingService(db).list_buildings()


@router.get("/{slug}", response_model=BuildingDetail)
def building_detail(slug: str, db: Session = Depends(get_db)):
    building = BuildingService(db).get_building_detail(slug)
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    return building
