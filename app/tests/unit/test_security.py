import pytest
from jose import jwt

from app.core.config import settings
from app.core.security import create_access_token, hash_password, verify_password


@pytest.mark.unit
def test_hash_and_verify_password():
    pw = "secret"
    try:
        h = hash_password(pw)
    except ValueError as e:
        pytest.skip(f"bcrypt backend not available: {e}")

    assert verify_password(pw, h)


@pytest.mark.unit
def test_create_access_token_contains_sub_and_exp():
    token = create_access_token({"sub": "42"})
    payload = jwt.decode(
        token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
    )
    assert payload["sub"] == "42"
    assert "exp" in payload
