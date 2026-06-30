from fastapi import APIRouter

from backend.services import human_review

router = APIRouter(
    prefix="/review",
    tags=["Review"]
)


@router.post("/{rfp_id}")
def review(
    rfp_id: int,
    approved: bool,
    comments: str = "",
):

    return human_review(
        rfp_id,
        approved,
        comments,
    )