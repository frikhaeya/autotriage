from fastapi import APIRouter
from pydantic import BaseModel
import httpx
import re

router = APIRouter()

class EmailInput(BaseModel):
    email_content: str
    username: str


def extract_most_recent_message(email_body: str) -> str:
    # known chain patterns first
    separators = [
        r"\n-{2,}Original Message-{2,}",
        r"\nOn .*wrote:",
        r"\n>?\s*From:\s"
    ]
    
    for pattern in separators:
        match = re.search(pattern, email_body)
        if match:
            return email_body[:match.start()].strip()

    return email_body.strip()



@router.post("/classify-email")
async def classify_email(input_data: EmailInput):
    url = "https://candidate-ds-endpoint.onrender.com/get-category"

    trimmed_content = extract_most_recent_message(input_data.email_content)

    payload = {
        "username": input_data.username,
        "email_content": trimmed_content
    }

    # Extend timeout to 60 seconds to accommodate slow ML endpoint
    timeout = httpx.Timeout(60.0)  

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
