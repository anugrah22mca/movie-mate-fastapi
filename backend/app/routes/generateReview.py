from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from openai import OpenAI
from pydantic import BaseModel
from typing import Optional
import os

# Load environment variables
load_dotenv()

# Initialize FastAPI router and OpenAI client
router = APIRouter()
client = OpenAI()

# Pydantic models
class Media(BaseModel):
    id: int
    title: str
    genre: Optional[str] = None
    platform: Optional[str] = None
    director: Optional[str] = None

class ReviewNote(BaseModel):
    reviewText: str
    media: Optional[Media] = None

# Endpoint to generate review
@router.post("/generate-review")
async def generate_review(data: ReviewNote):
    try:
        # Construct the prompt
        prompt = "Generate a short and engaging review for the following movie based on user notes."

        if data.media:
            prompt += f"\n\nTitle: {data.media.title}"
            if data.media.genre:
                prompt += f"\nGenre: {data.media.genre}"
            if data.media.director:
                prompt += f"\nDirector: {data.media.director}"
            if data.media.platform:
                prompt += f"\nAvailable on: {data.media.platform}"

        prompt += f"\n\nUser notes: {data.reviewText}"

        # OpenAI API call
        response = client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[
                {"role": "system", "content": "You're a helpful movie review assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.7
        )

        # Return response
        return {"review": response.choices[0].message.content.strip()}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
