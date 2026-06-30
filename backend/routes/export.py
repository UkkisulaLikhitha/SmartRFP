from fastapi import APIRouter
from fastapi.responses import Response

from utils.exporter import (
    export_pdf,
    export_docx,
    export_txt,
)

router = APIRouter(
    prefix="/export",
    tags=["Export"]
)


@router.get("/{rfp_id}/{fmt}")
def export(rfp_id: int, fmt: str):

    if fmt == "pdf":

        return Response(
            content=export_pdf(rfp_id),
            media_type="application/pdf",
            headers={
                "Content-Disposition":
                f'attachment; filename="proposal_{rfp_id}.pdf"'
            },
        )

    elif fmt == "docx":

        return Response(
            content=export_docx(rfp_id),
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={
                "Content-Disposition":
                f'attachment; filename="proposal_{rfp_id}.docx"'
            },
        )

    elif fmt == "txt":

        return Response(
            content=export_txt(rfp_id),
            media_type="text/plain",
            headers={
                "Content-Disposition":
                f'attachment; filename="proposal_{rfp_id}.txt"'
            },
        )

    return {
        "error": "Unsupported format"
    }