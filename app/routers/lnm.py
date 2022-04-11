from typing import List,Optional
from fastapi import APIRouter,Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Json

router = APIRouter(
    prefix="/payments",
    tags=["Payment Callback"]
)

class Payment(BaseModel):
    pass

@router.post("/confirmation")
async def process_payment(request: Request):
    print(f"request json {await request.json()}")
    return {"Message":"Callback hit!"}