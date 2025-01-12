import uuid
from datetime import datetime, timedelta
from typing import Optional

class APIKeyService:
    def __init__(self):
        self.api_keys = {}  # In-memory storage (replace with database in production)

    def create_api_key(self, user_id: str, expires_in_days: Optional[int] = 30) -> dict:
        """
        Create a new API key for a user
        """
        api_key = str(uuid.uuid4())
        expiration_date = datetime.utcnow() + timedelta(days=expires_in_days)
        
        key_data = {
            "api_key": api_key,
            "user_id": user_id,
            "created_at": datetime.utcnow(),
            "expires_at": expiration_date,
            "is_active": True
        }
        
        self.api_keys[api_key] = key_data
        return key_data

    def validate_api_key(self, api_key: str) -> bool:
        """
        Validate if an API key is valid and not expired
        """
        if api_key not in self.api_keys:
            return False
        
        key_data = self.api_keys[api_key]
        if not key_data["is_active"]:
            return False
            
        if datetime.utcnow() > key_data["expires_at"]:
            key_data["is_active"] = False
            return False
            
        return True

    def revoke_api_key(self, api_key: str) -> bool:
        """
        Revoke an API key
        """
        if api_key in self.api_keys:
            self.api_keys[api_key]["is_active"] = False
            return True
        return False

    def get_api_key_info(self, api_key: str) -> Optional[dict]:
        """
        Get information about an API key
        """
        return self.api_keys.get(api_key)