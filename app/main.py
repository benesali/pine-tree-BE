# app/main.py
from dotenv import load_dotenv
from fastapi import FastAPI

from app.api import apartments, auth, availability
from app.api.admin.calendar import router as admin_calendar_router

load_dotenv()

app = FastAPI(title="Pine Rent API")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(apartments.router, prefix="/apartments", tags=["apartments"])
app.include_router(availability.router, prefix="/apartments", tags=["availability"])
app.include_router(admin_calendar_router)

# app.include_router(subscriptions.router, prefix="/subscriptions",
# tags=["subscriptions"])


@app.get("/health")
def health():
    """Health check endpoint.

    Returns a simple JSON payload indicating the service is up. Useful for
    liveness probes and basic monitoring.

    Returns:
        dict: A status object with a single key `status` set to `ok`.
    """
    return {"status": "ok"}
