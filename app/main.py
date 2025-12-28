# app/main.py
from fastapi import FastAPI
from app.api import auth, apartments
from app.api import availability
from app.api.admin.calendar import router as admin_calendar_router

app = FastAPI(title="Pine Rent API")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(apartments.router, prefix="/apartments", tags=["apartments"])
app.include_router(availability.router, prefix="/apartments", tags=["availability"])
app.include_router(availability.router)
app.include_router(admin_calendar_router)

# app.include_router(subscriptions.router, prefix="/subscriptions", tags=["subscriptions"])



@app.get("/health")
def health():
    return {"status": "ok"}
