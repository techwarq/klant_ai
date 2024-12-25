

#make a endpoint that creates ai quotes
#make a end point that gets the user info 
#the user info will trigger the ai quotemaker and give back quotes to the frontend
#then the frontend will create a card plus a unique link to view the card
#the card can be shared
# give mack the link to the backend and the backend will create a email and sent to the user email


# main.py
from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import uuid
from aiosmtplib import send
from email.message import EmailMessage
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import os

# Initialize FastAPI app
app = FastAPI(title="Course Completion Card Service")

# Security setup for API keys
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

# Store API keys for different clients (in production, use a secure database)
API_KEYS = {
    "client1-key": "client1",
    "client2-key": "client2",
}

async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key in API_KEYS:
        return API_KEYS[api_key]
    raise HTTPException(
        status_code=403,
        detail="Invalid API key"
    )

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class PurchaseInfo(BaseModel):
    """Data received from the course seller's website"""
    user_name: str
    email: EmailStr
    course_name: str
    purchase_date: Optional[datetime] = None
    course_duration: Optional[str] = None
    custom_message: Optional[str] = None

class CardContent(BaseModel):
    """Response containing AI-generated content for the card"""
    card_id: str
    quote: str
    user_name: str
    course_name: str
    purchase_date: datetime
    course_duration: Optional[str]

class EmailRequest(BaseModel):
    """Data needed to send the email with the card link"""
    email: EmailStr
    card_url: str
    user_name: str
    course_name: str

# Initialize AI quote generator
groq_api_key = os.getenv("GROQ_API_KEY")
quote_generator = ChatGroq(api_key=groq_api_key)

quote_prompt = PromptTemplate(
    template="""Create an inspiring and motivational quote for someone who just purchased a course.
    Context:
    - Course Name: {course_name}
    - Student Name: {student_name}
    - Course Duration: {duration}
    
    Generate a short, engaging quote that:
    1. Congratulates them on their investment in learning
    2. Encourages them to make the most of the course
    3. Is positive and uplifting
    4. Is personal but professional
    
    Return the quote in JSON format with a 'quote' key.""",
    input_variables=["course_name", "student_name", "duration"]
)

json_parser = JsonOutputParser()

@app.post("/api/process-purchase", response_model=CardContent)
async def process_purchase(
    purchase_info: PurchaseInfo,
    client: str = Depends(get_api_key)
):
    """
    Endpoint that course sellers call when a purchase is completed.
    Returns data needed to create the celebration card.
    """
    try:
        # Generate AI quote
        chain = quote_prompt | quote_generator | json_parser
        quote_response = chain.invoke({
            "course_name": purchase_info.course_name,
            "student_name": purchase_info.user_name,
            "duration": purchase_info.course_duration or "not specified"
        })
        
        # Generate unique card ID
        card_id = str(uuid.uuid4())
        
        # Create card content response
        return CardContent(
            card_id=card_id,
            quote=quote_response["quote"],
            user_name=purchase_info.user_name,
            course_name=purchase_info.course_name,
            purchase_date=purchase_info.purchase_date or datetime.utcnow(),
            course_duration=purchase_info.course_duration
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
