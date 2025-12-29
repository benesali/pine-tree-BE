from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import create_access_token, verify_password
from app.db.session import get_db
from app.models.admin_user import AdminUser
from app.schemas.auth import AdminLoginRequest, AdminLoginResponse

router = APIRouter(tags=["auth"])


@router.post(
    "/login",
    response_model=AdminLoginResponse,
)
def login(
    data: AdminLoginRequest,
    db: Session = Depends(get_db),
):
    """Authenticate an admin and return a JWT access token.

    Args:
        data: `AdminLoginRequest` containing `email` and `password`.
        db: Database session for querying AdminUser records.

    Returns:
        dict: An access token response conforming to `AdminLoginResponse`.

    Raises:
        HTTPException: 401 when credentials are invalid.
    """
    user = db.query(AdminUser).filter(AdminUser.email == data.email).first()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.id)})

    return {
        "access_token": token,
        "token_type": "bearer",
    }
