from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from typing import Optional
import os

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

API_KEYS = {}

async def get_api_key(api_key: str = Security(api_key_header)) -> str:
    if api_key not in API_KEYS:
        raise HTTPException(status_code=403, details = "Invalid API key")
    return API_KEYS[api_key]