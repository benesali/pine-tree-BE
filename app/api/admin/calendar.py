from fastapi import HTTPException

@router.post("/block", response_model=CalendarRangeResponse)
def block_range(
    data: CalendarRangeBase,
    _: str = Depends(admin_required),
    db: Session = Depends(get_db),
):
    try:
        CalendarService(db).set_range(
            data.apartment_id,
            data.date_from,
            data.date_to,
            AvailabilityStatus.blocked,
            data.note,
        )
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

    return {"status": "blocked"}
