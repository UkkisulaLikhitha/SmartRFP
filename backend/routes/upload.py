from fastapi import APIRouter, UploadFile, File, Form
from backend.services import analyze_rfp

router = APIRouter()


@router.post("/upload-rfp")
async def upload_rfp(
    file: UploadFile = File(...),
    deal_name: str = Form(""),
    client_name: str = Form(""),
    region: str = Form(""),
    deadline: str = Form(""),
    assigned_role: str = Form(""),
    use_web_search: bool = Form(True),
):
    return await analyze_rfp(
        file=file,
        deal_name=deal_name,
        client_name=client_name,
        region=region,
        deadline=deadline,
        assigned_role=assigned_role,
        use_web_search=use_web_search,
    )