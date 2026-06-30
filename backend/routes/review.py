from fastapi import APIRouter
import database as db

router = APIRouter()




@router.put("/review/{rfp_id}")
def review(
    rfp_id: int,
    status: str,
):

    db.update_rfp_status(
        rfp_id,
        status
    )

    db.log_action(
        rfp_id,
        "Human Review",
        "Reviewer",
        status
    )

    return {
        "success": True
    }