from sqlalchemy import Column , Integer, string
from database import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime


class WebhookId(Base):
    __tablename__ = "webhookId"
    
    id = Column(Integer, primary_key=True, index=True)
    webhook_id = Column(String, unique=True, nullable=False)
    class WebhookId(Base):
        __tablename__ = "webhookId"
        
        id = Column(Integer, primary_key=True, index=True)
        webhook_id = Column(String, unique=True, nullable=False)
        created_at = Column(DateTime, default=datetime.utcnow)