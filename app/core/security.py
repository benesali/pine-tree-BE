"""Security helpers for password hashing and JWT handling."""

from datetime import UTC, datetime, timedelta
from typing import Any

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plain-text password and return the encoded hash.

    Args:
        password: The plain-text password to hash.

    Returns:
        The hashed password string.

    Raises:
        passlib.exceptions.*: Backend-specific errors may be raised if the hashing
        backend is not available.
    """
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    """Verify a plain-text password against a stored hash value.

    Args:
        password: The plain-text password to verify.
        hashed: The stored hashed password to compare against.

    Returns:
        True if the password matches the hash, False otherwise.
    """
    return pwd_context.verify(password, hashed)


def create_access_token(data: dict[str, Any]) -> str:
    """Create a JWT access token containing the provided claims.

    Args:
        data: Dictionary of claims to include in the token.

    Returns:
        The encoded JWT string.
    """
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
