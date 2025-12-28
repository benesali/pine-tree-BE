from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.general_dependency import get_db
from app.core.security import verify_password, create_access_token
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
    user = (
        db.query(AdminUser)
        .filter(AdminUser.email == data.email)
        .first()
    )

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.id)})

    return {
        "access_token": token,
        "token_type": "bearer",
    }
