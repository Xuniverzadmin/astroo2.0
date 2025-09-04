from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .core import analyze_name
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(panchangam_router)

app = FastAPI(title="Astrooverz API", version="1.0.0")

app.include_router(auth.router)
app.include_router(profiles.router)
app.include_router(store.router)
app.include_router(astro.router)
app.include_router(llm.router)

@app.get("/")
def root():
    return {"message": "Astrooverz Numerology API", "status": "running"}

@app.get("/healthz")
def healthz():
    return {"ok": True, "status": "healthy", "service": "numerology-api"}

@app.get("/api/healthz")
def api_healthz():
    return {"ok": True, "status": "healthy", "service": "numerology-api"}

@app.post("/api/analyze_name")
def analyze_name_endpoint(payload: NameIn):
    try:
        if not payload.name or not payload.name.strip():
            raise HTTPException(status_code=400, detail="Name cannot be empty")
        
        result = analyze_name(payload.name.strip())
        logger.info(f"Successfully analyzed name: {payload.name}")
        return result
    except Exception as e:
        logger.error(f"Error analyzing name '{payload.name}': {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during name analysis")

@app.get("/api/analyze_name/{name}")
def analyze_name_get(name: str):
    try:
        if not name or not name.strip():
            raise HTTPException(status_code=400, detail="Name cannot be empty")
        
        result = analyze_name(name.strip())
        logger.info(f"Successfully analyzed name: {name}")
        return result
    except Exception as e:
        logger.error(f"Error analyzing name '{name}': {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during name analysis")
