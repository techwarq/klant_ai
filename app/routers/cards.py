from fastapi import APIRouter, Depends, BackgroundTasks
from app.auth import get_api_key
from app.services.card_service import generate_card
from app.models.purchase import PurchaseInfo
from app.models.card import CardContent

router = APIRouter()

@router.post("/api/cards/generate", response_model=CardContent)
async def generate_card_route(
    purchase: PurchaseInfo,
    background_tasks: BackgroundTasks,
    client: str = Depends(get_api_key)
):
    return generate_card(purchase, client)
