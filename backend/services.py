from fastapi import UploadFile

from backend.database import SessionLocal
from backend import crud

from utils.file_handler import extract_text
from pipeline import run_pipeline


# ==========================================================
# Upload & Analyze
# ==========================================================

async def analyze_rfp(
    file: UploadFile,
    deal_name: str,
    client_name: str,
    region: str,
    deadline: str,
    assigned_role: str,
    use_web_search: bool,
):

    contents = await file.read()

    raw_text = extract_text(
        file.filename,
        contents,
    )

    db = SessionLocal()

    try:

        rfp_id = crud.create_rfp(
            db=db,
            deal_name=deal_name or file.filename,
            client_name=client_name,
            region=region,
            deadline=deadline,
            contact_email="",
            notes="",
            file_name=file.filename,
            raw_text=raw_text,
            assigned_role=assigned_role,
            assigned_to="",
            use_web_search=use_web_search,
        )

    finally:
        db.close()

    result = run_pipeline(
        rfp_id=rfp_id,
        raw_text=raw_text,
        use_web_search=use_web_search,
        progress=None,
    )

    return {
        "success": True,
        "rfp_id": rfp_id,
        "result": result,
    }


# ==========================================================
# Pricing
# ==========================================================

def calculate_resource_cost(rfp_id: int):

    db = SessionLocal()

    try:

        pricing = crud.get_pricing(
            db,
            rfp_id,
        )

        return {
            "rfp_id": rfp_id,
            "pricing": pricing,
        }

    finally:
        db.close()


# ==========================================================
# Human Review
# ==========================================================

def human_review(
    rfp_id: int,
    approved: bool,
    comments: str,
):

    db = SessionLocal()

    try:

        rfp = crud.get_rfp(
            db,
            rfp_id,
        )

        if not rfp:

            return {
                "success": False,
                "message": "RFP not found",
            }

        rfp.status = "Approved" if approved else "Rejected"

        db.commit()

        crud.log_action(
            db,
            rfp_id,
            "Human Review",
            "Reviewer",
            comments,
        )

        return {
            "success": True,
            "status": rfp.status,
            "comments": comments,
        }

    finally:
        db.close()


# ==========================================================
# Export
# ==========================================================

def export_project(
    rfp_id: int,
    export_format: str,
):

    db = SessionLocal()

    try:

        draft = crud.get_draft_sections(
            db,
            rfp_id,
        )

        return {
            "rfp_id": rfp_id,
            "format": export_format,
            "draft": draft,
        }

    finally:
        db.close()


# ==========================================================
# Regenerate Draft
# ==========================================================

def regenerate_pipeline(
    rfp_id: int,
):

    db = SessionLocal()

    try:

        rfp = crud.get_rfp(
            db,
            rfp_id,
        )

        if not rfp:

            return {
                "success": False,
                "message": "RFP not found",
            }

        run_pipeline(
            rfp_id=rfp.id,
            raw_text=rfp.raw_text,
            use_web_search=rfp.use_web_search,
            progress=None,
        )

        crud.log_action(
            db,
            rfp.id,
            "Draft Regenerated",
            "FastAPI",
        )

        return {
            "success": True,
            "message": "Draft regenerated successfully",
        }

    finally:
        db.close()