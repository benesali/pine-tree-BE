from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Yield a database session for use as a FastAPI dependency.

    The session is created from `SessionLocal` and is closed when the
    dependency is torn down (after the request completes).

    Yields:
        Session: A SQLAlchemy session instance bound to the configured engine.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
