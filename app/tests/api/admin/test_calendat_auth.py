from app.core.security import create_access_token
from app.models.admin_user import AdminUser


VALID_PAYLOAD = {
    "apartment_id": 1,
    "date_from": "2025-07-10",
    "date_to": "2025-07-12",
}


def test_missing_token_returns_401(client):
    resp = client.post("/admin/calendar/block", json=VALID_PAYLOAD)
    assert resp.status_code == 401


def test_nonexistent_admin_returns_403(client):
    token = create_access_token({"sub": "99999"})

    resp = client.post(
        "/admin/calendar/block",
        headers={"Authorization": f"Bearer {token}"},
        json=VALID_PAYLOAD,
    )

    assert resp.status_code == 403


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
