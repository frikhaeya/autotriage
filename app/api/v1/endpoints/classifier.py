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

    # Extend timeout to 30 seconds to accommodate slow ML endpoint
    timeout = httpx.Timeout(30.0)  

    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            result = response.json()
            return {"category": result.get("category", "No category returned")}
        except httpx.HTTPError as e:
            return {"error": f"HTTP error: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
