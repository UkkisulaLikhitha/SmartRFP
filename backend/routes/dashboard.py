from fastapi import APIRouter
import database as db

router = APIRouter()


@router.get("/dashboard")
def dashboard():

    rfps = db.list_rfps()

    return {
        "projects": rfps
    }


@router.get("/dashboard/{rfp_id}")
def dashboard_details(rfp_id: int):

    return {
        "rfp": db.get_rfp(rfp_id),
        "requirements": db.get_requirements(rfp_id),
        "draft": db.get_draft_sections(rfp_id),
        "pricing": db.get_pricing(rfp_id),
        "evaluation": db.get_evaluation_metrics(rfp_id),
        "audit": db.get_audit_log(rfp_id),
    }