from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse
from typing import Optional
from ..schemas import UssdResponse
from fastapi.params import Depends
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db

# create a simple callback url that prints out all ussd parameters from at
router = APIRouter(
    prefix="/ussd",
    tags=["Ussd callback"]
)


async def process_response(resp: str, phone_number: str):
    response: str = ""
    # get user by phonenumber and send greeting
    # print(resp)

    # user = await ussd.get_user(phone_number)
    user = {
        "name": "Daniel"
    }
    #print(f"user: {user}")
    if len(resp) <= 1:
        if resp == "":
            if user:
                response = f"CON Hello {user['name']}\n"
                response += "1. Query Bill \n"
                response += "2. Exit"
            else:
                response = f"CON Hello!"
                response += "1. Query Bill \n"
                response += "2. Exit"
        elif resp == "1":
            response = "CON Feature to be implemented"
        elif resp == "2":
            response = "END Thank you for using this service!"
    return response


@router.post("/callback", response_class=HTMLResponse)
async def ussd_callback(session_id: str = Form(""), service_code: str = Form(""), phone_number: str = Form(""), text: Optional[str] = Form("")):
    # get user inside route
    print(f"phone_no: {phone_number}")
    print(f"text: {text}")
    """
    user = db.query(models.User).filter(
        models.User.phonenumber == phone_number).first()
    print(user)
    """
    return await process_response(text, phone_number)
