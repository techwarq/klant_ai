from sqlalchemy import Column, Integer, String, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class APIKey(Base):
    __tablename__ = "api_keys"
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)
    client_name = Column(String)
    
class WebhookRegistration(Base):
    __tablename__ = "webhooks"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    events = Column(JSON)
    secret_key = Column(String)
    is_active = Column(Boolean, default=True)
    client_id = Column(Integer, ForeignKey('api_keys.id'))
    client = relationship("APIKey", back_populates="webhooks")

APIKey.webhooks = relationship("WebhookRegistration", back_populates="client")
