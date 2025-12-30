# app/main.py
from dotenv import load_dotenv
from fastapi import FastAPI

from app.api import apartments, auth, availability, buildings
from app.api.admin.calendar import router as admin_calendar_router

load_dotenv()

app = FastAPI(title="Pine Rent API")

# Auth (PUBLIC)
app.include_router(
    auth.router,
    prefix="/api/auth",
    tags=["auth"],
)

# Apartments (PUBLIC)
app.include_router(
    apartments.router,
    prefix="/api/apartments",
    tags=["apartments"],
)

# Availability (PUBLIC)
app.include_router(
    availability.router,
    prefix="/api/availability",
    tags=["availability"],
)

# Admin calendar (PROTECTED)
app.include_router(
    admin_calendar_router,
    prefix="/api/admin/calendar",
    tags=["admin"],
)
# Buildings (PUBLIC)
app.include_router(
    buildings.router,
    prefix="/api/buildings",
    tags=["buildings"],
)


@app.get("/health")
def health():
    return {"status": "ok"}
