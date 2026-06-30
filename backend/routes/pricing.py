from fastapi import APIRouter

from backend.services import calculate_resource_cost

router = APIRouter(
    prefix="/pricing",
    tags=["Pricing"]
)


@router.get("/{rfp_id}")
def pricing(rfp_id: int):
    return calculate_resource_cost(rfp_id)