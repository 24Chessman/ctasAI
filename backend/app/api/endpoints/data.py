# app/api/endpoints/data.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_data():
    return {"message": "Data endpoint is working"}

# You can add more data-related endpoints here later