from fastapi import APIRouter

from backend.services import regenerate_pipeline

router = APIRouter(
    prefix="/regenerate",
    tags=["Pipeline"]
)


@router.post("/{rfp_id}")
def regenerate(rfp_id: int):
    return regenerate_pipeline(rfp_id)