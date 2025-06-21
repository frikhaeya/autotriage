from fastapi import APIRouter
from pydantic import BaseModel
import httpx 

router = APIRouter()

class EmailInput(BaseModel):
    email_content: str
    username: str

@router.post("/classify-email")
async def classify_email(input_data: EmailInput):
    url = "https://candidate-ds-endpoint.onrender.com/get-category"
    payload = {
        "username": input_data.username,
        "email_content": input_data.email_content
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            return {"category": response.json().get("category")}
        except httpx.HTTPError as e:
            return {"error": str(e)}
