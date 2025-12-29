from datetime import date

import pytest
from pydantic import ValidationError

from app.models.availability import AvailabilityStatus
from app.schemas.auth import AdminLoginRequest, AdminLoginResponse
from app.schemas.availability import AvailabilityDay
from app.schemas.calendar import CalendarActionResponse, CalendarRangeRequest


@pytest.mark.unit
def test_admin_login_request_validates_email():
    with pytest.raises(ValidationError):
        AdminLoginRequest(email="not-an-email", password="x")


@pytest.mark.unit
def test_admin_login_response_defaults():
    r = AdminLoginResponse(access_token="tok")
    assert r.token_type == "bearer"
    assert r.dict()["access_token"] == "tok"


@pytest.mark.unit
def test_availability_day_parses_enum_and_date():
    payload = {"date": "2025-07-10", "status": "blocked"}
    d = AvailabilityDay(**payload)
    assert isinstance(d.date, date)
    assert d.status == AvailabilityStatus.blocked


@pytest.mark.unit
def test_calendar_range_request_accepts_dates():
    data = {"apartment_id": 1, "date_from": "2025-07-10", "date_to": "2025-07-12"}
    cr = CalendarRangeRequest(**data)
    assert cr.apartment_id == 1
    assert isinstance(cr.date_from, date)


@pytest.mark.unit
def test_calendar_range_validation_rejects_inverted_dates():
    data = {"apartment_id": 1, "date_from": "2025-07-12", "date_to": "2025-07-10"}
    with pytest.raises(ValueError):
        CalendarRangeRequest(**data)


@pytest.mark.unit
def test_calendar_action_response():
    res = CalendarActionResponse(status="blocked")
    assert res.status == "blocked"
