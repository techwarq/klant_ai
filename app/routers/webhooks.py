from fastapi import APIRouter, Depends
from app.auth import get_api_key
from app.database import webhooks_db
from app.models.webhook import WebhookRegistration
import uuid

router = APIRouter()

@router.post("/api/webhooks/register")
async def register_webhook(
    webhook: WebhookRegistration,
    client: str = Depends(get_api_key)
):
    webhook_id = str(uuid.uuid4())
    webhooks_db[webhook_id] = webhook.dict() | {"client": client}
    return {"webhook_id": webhook_id}
