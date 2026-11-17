from fastapi import APIRouter
from app.schemas.meeting import ModelsResponse
from app.services.ollama import list_local_models

router = APIRouter()


@router.get("/models", response_model=ModelsResponse)
async def models():
    return {"models": await list_local_models()}
