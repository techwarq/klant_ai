from fastapi import FastAPI, HTTPException
import BaseModel
from typing import List, Optional
from fastapi import APIRouter
from datetime import datetime

class WebhookRegistration(BaseModel):
    url: str
    events: List[str]
    secret_key: str

class Webhook(BaseModel):
    id: str
    url: str
    events: List[str]
    secret_key: str
    active: bool = True
    created_at: datetime
    router = APIRouter()

    webhooks = []

    @router.post("/webhooks")
    async def register_webhook(webhook: WebhookRegistration):
        webhook_id = str(uuid.uuid4())
        new_webhook = Webhook(
            id=webhook_id,
            url=webhook.url,
            events=webhook.events,
            secret_key=webhook.secret_key,
            created_at=datetime.utcnow()
        )
        webhooks.append(new_webhook)
        return new_webhook

    @router.get("/webhooks")
    async def list_webhooks():
        return webhooks

    @router.delete("/webhooks/{webhook_id}")
    async def delete_webhook(webhook_id: str):
        for webhook in webhooks:
            if webhook.id == webhook_id:
                webhooks.remove(webhook)
                return {"message": "Webhook deleted"}
        raise HTTPException(status_code=404, detail="Webhook not found")