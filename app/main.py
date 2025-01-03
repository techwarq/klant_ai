from fastapi import FastAPI
from app.routers import api_keys, webhooks, cards

app = FastAPI(title="Course Celebration card serveice")

app.include_router(api_keys.router)
app.include_router(webhooks.router)
app.include_router(cards.router)