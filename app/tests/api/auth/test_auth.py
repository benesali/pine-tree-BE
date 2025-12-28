from unittest.mock import MagicMock
from app.models.admin_user import AdminUser


def test_login_success(client, mock_db):
    user = AdminUser(
        id=1,
        email="admin@test.cz",
        password_hash="hashed",
    )

    mock_db.query.return_value.filter.return_value.first.return_value = user

    from app.core.security import verify_password
    verify_password_mock = lambda plain, hashed: True

    # monkeypatch funkce
    import app.api.auth as auth_module
    auth_module.verify_password = verify_password_mock

    response = client.post(
        "/login",
        json={"email": "admin@test.cz", "password": "secret"},
    )

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_invalid_credentials(client, mock_db):
    mock_db.query.return_value.filter.return_value.first.return_value = None

    response = client.post(
        "/login",
        json={"email": "xxx@test.cz", "password": "wrong"},
    )

    assert response.status_code == 401


