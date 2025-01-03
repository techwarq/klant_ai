from fastapi import APIRouter, Depends
from app.auth import get_api_key
from app.database import API_KEYS
from app.models.api_key import APIKeyRequest
import uuid

router = APIRouter()

@router.post("/api/keys/generate")
async def generate_api_key(request: APIKeyRequest):
    api_key = str(uuid.uuid4())
    API_KEYS[api_key] = request.client_name
    return {"api_key": api_key}
