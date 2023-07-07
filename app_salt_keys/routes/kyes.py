from fastapi import APIRouter, Depends, HTTPException
from fastapi.security.api_key import APIKey
from pydantic import BaseModel
from app_salt_keys.auth import get_api_key

router = APIRouter(
    prefix="/api/v1",
    tags=["keys"],
    dependencies = [Depends(get_api_key)],
)


@router.get("/keys/{key}")
def info(key: str):
    return { "geting": key }

#api_key: APIKey = Depends(get_api_key))