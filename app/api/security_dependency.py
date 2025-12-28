from fastapi import Depends, HTTPException, Header
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.core.config import settings
from app.api.general_dependency import get_db
from app.models.admin_user import AdminUser


def admin_required(authorization: str = Header(...), db: Session = Depends(get_db)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401)

    token = authorization.replace("Bearer ", "")
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
            raise HTTPException(status_code=401)

        user = db.query(AdminUser).filter(AdminUser.id == admin_id).first()
        if not user or not user.is_active:
            raise HTTPException(status_code=403)

        return str(user.id)
    except JWTError:
        raise HTTPException(status_code=401)
