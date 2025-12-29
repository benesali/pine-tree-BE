from datetime import date

import pytest

from app.core.security import create_access_token
from app.models.admin_user import AdminUser
from app.models.availability import Availability, AvailabilityStatus

VALID_PAYLOAD = {
    "apartment_id": 1,
    "date_from": "2025-07-10",
    "date_to": "2025-07-12",
}


@pytest.mark.unit
def test_missing_token_returns_401(client):
    resp = client.post("/admin/calendar/block", json=VALID_PAYLOAD)
    assert resp.status_code == 401


@pytest.mark.unit
def test_nonexistent_admin_returns_403(client):
    token = create_access_token({"sub": "99999"})

    resp = client.post(
        "/admin/calendar/block",
        headers={"Authorization": f"Bearer {token}"},
        json=VALID_PAYLOAD,
    )

    assert resp.status_code == 403


@pytest.mark.integration
def test_inactive_admin_returns_403(client, db):
    admin = AdminUser(
        email="inactive@test.cz",
        password_hash="x",
        is_active=False,
    )
    db.add(admin)
    db.commit()

    token = create_access_token({"sub": str(admin.id)})

    resp = client.post(
        "/admin/calendar/block",
        headers={"Authorization": f"Bearer {token}"},
        json=VALID_PAYLOAD,
    )

    assert resp.status_code == 403


@pytest.mark.integration
def test_active_admin_allowed(client, db):
    admin = AdminUser(
        email="active@test.cz",
        password_hash="x",
        is_active=True,
    )
    db.add(admin)
    db.commit()

    token = create_access_token({"sub": str(admin.id)})

    resp = client.post(
        "/admin/calendar/block",
        headers={"Authorization": f"Bearer {token}"},
        json=VALID_PAYLOAD,
    )

    assert resp.status_code == 200


@pytest.mark.integration
def test_block_range_conflict_with_booked_returns_409(client, db):
    # create active admin
    admin = AdminUser(email="admin@t.cz", password_hash="x", is_active=True)
    db.add(admin)
    db.commit()

    # seed a booked availability on 2025-07-11
    booked_day = date(2025, 7, 11)
    db.add(
        Availability(apartment_id=1, date=booked_day, status=AvailabilityStatus.booked)
    )
    db.commit()

    token = create_access_token({"sub": str(admin.id)})

    resp = client.post(
        "/admin/calendar/block",
        headers={"Authorization": f"Bearer {token}"},
        json={"apartment_id": 1, "date_from": "2025-07-10", "date_to": "2025-07-12"},
    )

    assert resp.status_code == 409
