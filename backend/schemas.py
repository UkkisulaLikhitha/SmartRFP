from typing import Optional, Dict, Any
from pydantic import BaseModel


class AnalyzeResponse(BaseModel):
    success: bool
    result: Dict[str, Any]


class ResourceCostRequest(BaseModel):
    project_id: str


class HumanReviewRequest(BaseModel):
    project_id: str
    approved: bool
    comments: Optional[str] = ""


class ExportRequest(BaseModel):
    project_id: str
    format: str = "pdf"