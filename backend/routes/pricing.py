from fastapi import APIRouter
import database as db

router = APIRouter()


@router.get("/pricing/{rfp_id}")
def pricing(rfp_id: int):

    return db.get_pricing(rfp_id)