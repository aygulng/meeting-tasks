from fastapi import APIRouter
from app.schemas.meeting import ExtractRequest, ExtractResponse
from app.services.extraction import extract_tasks

router = APIRouter()


@router.post("/extract", response_model=ExtractResponse)
async def extract(request: ExtractRequest):
    return await extract_tasks(request)
