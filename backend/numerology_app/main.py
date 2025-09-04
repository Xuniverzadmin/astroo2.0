from __future__ import annotations

from fastapi import FastAPI

from .db import engine, Base

# Import routers
from .api_chat import router as chat_router
from .api_store import router as store_router
from .api_astro import router as astro_router
from .api_llm import router as llm_router
from .api_auth import router as auth_router
from .api_profiles import router as profiles_router
from .api_calendar import router as calendar_router
from .api_billing import router as billing_router
from .api_panchangam import router as panchangam_router


app = FastAPI(title="Astrooverz API")


@app.on_event("startup")
def on_startup() -> None:
    """Create database tables on startup. For production, prefer Alembic migrations."""
    Base.metadata.create_all(bind=engine)


# Mount all API routers under /api
for router in (
    chat_router,
    store_router,
    astro_router,
    llm_router,
    auth_router,
    profiles_router,
    calendar_router,
    billing_router,
    panchangam_router,
):
    app.include_router(router, prefix="/api")


@app.get("/healthz")
def healthz() -> dict[str, bool]:
    return {"ok": True}
