from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.admin_user import AdminUser


def main():
    db: Session = SessionLocal()

    email = "XXX"
    password = "XXX"  # noqa S105

    existing = db.query(AdminUser).filter(AdminUser.email == email).first()
    if existing:
        print("Admin user already exists")
        return

    admin = AdminUser(
        email=email,
        password_hash=hash_password(password),
        is_active=True,
    )

    db.add(admin)
    db.commit()

    print("Admin user created")
    print("Email:", email)
    print("Password:", password)


if __name__ == "__main__":
    main()
