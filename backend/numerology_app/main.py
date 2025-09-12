from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import engine, Base, check_database_connection
from .migrations.initial_schema import create_initial_schema
from .jobs import initialize_jobs, cleanup_jobs
from .config import settings

# Import main API router
from .api import router as api_router
from .api_chat import router as chat_router
from .api_store import router as store_router
from .api_astro import router as astro_router
from .api_llm import router as llm_router
from .api_auth import router as auth_router
from .api_profiles import router as profiles_router
from .api_calendar import router as calendar_router
from .api_billing import router as billing_router
from .api_panchangam import router as panchangam_router
from .api_quick_reading import router as quick_reading_router
from .api_birth_chart import router as birth_chart_router
from .api_dasha import router as dasha_router
from .api_events import router as events_router
from .api_interpretation import router as interpretation_router


app = FastAPI(title="Astrooverz API")

# Add CORS middleware - guaranteed working configuration
import os

# Robust CORS origins
origins_env = os.getenv("CORS_ORIGINS", "")
origins = [o.strip() for o in origins_env.split(",") if o.strip()] or [
    "https://astrooverz.com",
    "https://www.astrooverz.com",
    "http://localhost:5173",
]

# Debug logging for CORS origins
import logging
logger = logging.getLogger(__name__)
logger.info(f"CORS origins configured: {origins}")
logger.info(f"CORS_ORIGINS env var: {origins_env}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup() -> None:
    """Initialize database and create tables on startup."""
    try:
        # Check database connection
        if not check_database_connection():
            raise Exception("Database connection failed during startup")
        
        # Create initial schema
        create_initial_schema()
        
        # Initialize job system if enabled and in production
        if settings.SCHED_ENABLED:
            await initialize_jobs()
        
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Startup failed: {str(e)}")
        # Don't raise here to allow the app to start even if some services are unavailable


@app.on_event("shutdown")
async def on_shutdown() -> None:
    """Cleanup resources on shutdown."""
    try:
        if settings.SCHED_ENABLED:
            await cleanup_jobs()
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Shutdown cleanup failed: {str(e)}")


# Mount all API routers under /api
# Main API router (contains /ask, /auth/login, /readings/mini endpoints)
app.include_router(api_router, prefix="/api")

# Mount all other API routers under /api
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
    quick_reading_router,
    birth_chart_router,
    dasha_router,
    events_router,
    interpretation_router,
):
    app.include_router(router, prefix="/api")


@app.get("/healthz")
def healthz() -> dict[str, bool]:
    return {"ok": True}

@app.get("/api/healthz")
def api_healthz() -> dict[str, str | bool]:
    return {"ok": True, "status": "healthy", "service": "numerology-api"}

