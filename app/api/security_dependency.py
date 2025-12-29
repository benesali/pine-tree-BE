from fastapi import Depends, Header, HTTPException
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.admin_user import AdminUser


def admin_required(
    authorization: str | None = Header(None),
    db: Session = Depends(get_db),
):
    """FastAPI dependency to require an active admin user.

    Validates the Authorization header contains a Bearer token, decodes the
    JWT, and verifies the `sub` claim corresponds to an active AdminUser.

    Args:
        authorization: The Authorization header value (expects 'Bearer <token>').
        db: The database session provided by the `get_db` dependency.

    Returns:
        The admin user's id as a `str` when the token is valid and the user is active.

    Raises:
        HTTPException: 401 for missing/invalid token, or 403 for inactive or
            non-existent admins.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401)

    token = authorization.replace("Bearer ", "", 1)

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )

        sub = payload.get("sub")
        if not sub:
            raise HTTPException(status_code=401)

        try:
            admin_id = int(sub)
        except (TypeError, ValueError):
            raise HTTPException(status_code=401) from None

        user = db.query(AdminUser).filter(AdminUser.id == admin_id).first()

        if not user or not user.is_active:
            raise HTTPException(status_code=403)

        return str(user.id)

    except JWTError:
        raise HTTPException(status_code=401) from None
