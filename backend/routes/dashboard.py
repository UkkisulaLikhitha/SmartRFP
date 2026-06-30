from fastapi import APIRouter, HTTPException

from backend.database import SessionLocal
from backend import crud

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/rfps")
def list_rfps():

    db = SessionLocal()

    try:
        return crud.list_rfps(db)

    finally:
        db.close()


@router.get("/rfps/{rfp_id}")
def get_rfp(rfp_id: int):

    db = SessionLocal()

    try:

        rfp = crud.get_rfp(db, rfp_id)

        if not rfp:
            raise HTTPException(status_code=404, detail="Not Found")

        return rfp

    finally:
        db.close()