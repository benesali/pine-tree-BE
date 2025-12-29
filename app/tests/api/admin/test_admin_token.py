import pytest
from jose import jwt

from app.core.config import settings
from app.core.security import create_access_token

pytestmark = pytest.mark.unit


@pytest.mark.unit
def test_invalid_sub_returns_401(client):
    # sub that cannot be converted to int
    token = create_access_token({"sub": "not-an-int"})

    resp = client.post(
        "/admin/calendar/block",
        headers={"Authorization": f"Bearer {token}"},
        json={"apartment_id": 1, "date_from": "2025-07-10", "date_to": "2025-07-10"},
    )

    assert resp.status_code == 401


@pytest.mark.unit
def test_expired_token_returns_401(client):
    # Build a token with an exp in the past
    expired = jwt.encode(
        {"sub": "1", "exp": 0}, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
    )

    resp = client.post(
        "/admin/calendar/block",
        headers={"Authorization": f"Bearer {expired}"},
        json={"apartment_id": 1, "date_from": "2025-07-10", "date_to": "2025-07-10"},
    )

    assert resp.status_code == 401
