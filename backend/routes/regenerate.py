from fastapi import APIRouter
from pydantic import BaseModel

from backend.services import regenerate_pipeline

router = APIRouter()


class RegenerateRequest(BaseModel):
    rfp_id: int


@router.post("/regenerate")
async def regenerate(request: RegenerateRequest):
    return regenerate_pipeline(request.rfp_id)