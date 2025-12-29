# app/init_db.py
import app.models as _models  # noqa: F401
from app.db.session import Base, engine

Base.metadata.create_all(bind=engine)
