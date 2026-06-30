from fastapi import APIRouter
import database as db

router = APIRouter()


@router.get("/export/{rfp_id}")
def export(rfp_id: int):

    return {
        "rfp": db.get_rfp(rfp_id),
        "sections": db.get_draft_sections(rfp_id),
        "pricing": db.get_pricing(rfp_id)
    }