from fastapi import APIRouter

from app.api.v1.endpoints import emails, classifier

api_router = APIRouter()

api_router.include_router(emails.router, prefix="/emails", tags=["emails"])

api_router.include_router(classifier.router, prefix="/classifier", tags=["classifier"])
