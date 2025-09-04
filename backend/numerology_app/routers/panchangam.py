from fastapi import APIRouter, Depends
from ..schemas.panchangam import PanchangamQuery, PanchangamOut
from ..services.panchangam_service import get_panchangam
from ..core.deps import get_cache, get_settings

router = APIRouter()

@router.get("/panchangam", response_model=PanchangamOut)
async def panchangam_endpoint(q: PanchangamQuery = Depends(),
                              cache = Depends(get_cache),
                              settings = Depends(get_settings)):
    return await get_panchangam(q, cache=cache, settings=settings)
