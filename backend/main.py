from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend import crud
from backend.models import *

from pipeline import run_pipeline

app = FastAPI(
    title="SmartRFP API",
    version="1.0.0",
    description="Backend API for SmartRFP"
)

# Allow Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {
        "message": "SmartRFP API Running"
    }


###########################################################################
# Upload RFP
###########################################################################

@app.post("/upload")
async def upload_rfp(file: UploadFile = File(...)):

    text = (await file.read()).decode("utf-8", errors="ignore")

    db: Session = SessionLocal()

    try:

        rfp_id = crud.create_rfp(
            db=db,
            deal_name=file.filename,
            client_name="",
            region="",
            deadline="",
            contact_email="",
            notes="",
            file_name=file.filename,
            raw_text=text,
            assigned_role="",
            assigned_to="",
            use_web_search=True
        )

        # crud.create_rfp already commits and returns the new RFP's id (int)
        return {
            "rfp_id": rfp_id,
            "message": "Uploaded Successfully"
        }

    finally:
        db.close()


###########################################################################
# Run Pipeline
###########################################################################

@app.post("/pipeline/{rfp_id}")
def execute_pipeline(rfp_id: int):

    db = SessionLocal()

    try:

        rfp = crud.get_rfp(db, rfp_id)

        if not rfp:
            raise HTTPException(
                status_code=404,
                detail="RFP not found"
            )

        result = run_pipeline(
            rfp.id,
            rfp.raw_text,
            rfp.use_web_search
        )

        return result

    finally:
        db.close()


###########################################################################
# Dashboard
###########################################################################

@app.get("/rfps")
def list_rfps():

    db = SessionLocal()

    try:

        data = crud.list_rfps(db)

        return data

    finally:
        db.close()


###########################################################################
# Single RFP
###########################################################################

@app.get("/rfps/{rfp_id}")
def get_rfp(rfp_id: int):

    db = SessionLocal()

    try:

        rfp = crud.get_rfp(db, rfp_id)

        if not rfp:

            raise HTTPException(
                status_code=404,
                detail="Not Found"
            )

        return rfp

    finally:
        db.close()


###########################################################################
# Requirements
###########################################################################

@app.get("/requirements/{rfp_id}")
def get_requirements(rfp_id: int):

    db = SessionLocal()

    try:

        return crud.get_requirements(
            db,
            rfp_id
        )

    finally:
        db.close()


###########################################################################
# Draft Sections
###########################################################################

@app.get("/draft/{rfp_id}")
def get_draft(rfp_id: int):

    db = SessionLocal()

    try:

        return crud.get_draft_sections(
            db,
            rfp_id
        )

    finally:
        db.close()


###########################################################################
# Pricing
###########################################################################

@app.get("/pricing/{rfp_id}")
def get_pricing(rfp_id: int):

    db = SessionLocal()

    try:

        return crud.get_pricing(
            db,
            rfp_id
        )

    finally:
        db.close()


###########################################################################
# Evaluation
###########################################################################

@app.get("/evaluation/{rfp_id}")
def evaluation(rfp_id: int):

    db = SessionLocal()

    try:

        return crud.get_evaluation_metrics(
            db,
            rfp_id
        )

    finally:
        db.close()


###########################################################################
# Audit Log
###########################################################################

@app.get("/audit/{rfp_id}")
def audit(rfp_id: int):

    db = SessionLocal()

    try:

        return crud.get_audit_log(
            db,
            rfp_id
        )

    finally:
        db.close()


###########################################################################
# Delete
###########################################################################

@app.delete("/rfps/{rfp_id}")
def delete_rfp(rfp_id: int):

    db = SessionLocal()

    try:

        crud.delete_rfp(
            db,
            rfp_id
        )

        db.commit()

        return {
            "message": "Deleted Successfully"
        }

    finally:
        db.close()