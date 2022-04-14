import datetime
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


def generate_greeting():
    hour = datetime.datetime.now().hour
    greeting = "Good morning" if 5 <= hour < 12 else "Good afternoon" if hour < 18 else "Good evening"
    return greeting


async def process_response(resp: str, user):
    response: str = ""
    if len(resp) <= 1:
        # top level menu
        if resp == "":
            # The first request.
            if user:
                response = f"CON {generate_greeting()} {user.name} please select an option\n"
                response += "1. query Bill \n"
                response += "2. exit"
            else:
                response = f"CON {generate_greeting()} please select an option\n"
                response += "1. query Bill \n"
                response += "2. exit"
        elif resp == "1":
            if user:
                response = "CON Choose the unit account\n"
                for i, unit in enumerate(user.units):
                    response += f"{i+1}. unitid{user.units[i].id}\n"
                response += f"{len(user.units)+1}. enter a different unit id\n"
                response += f"{len(user.units)+2}. exit\n"
            else:
                response = "CON Please enter the unit id for your account\n"
            #response += f"UnitID:{user.units}\n"
        elif resp == "2":
            response = "END Thank you for using this service!"
    elif len(resp) == 3:
        pass
    else:
        pass
    return response


@router.post("/callback", response_class=HTMLResponse)
async def ussd_callback(sessionId: str = Form(""), serviceCode: str = Form(""), phoneNumber=Form(""), text: Optional[str] = Form(""), db: Session = Depends(get_db)):
    # get user inside route
    print(f"session_id: {sessionId}")
    print(f"service_code: {serviceCode}")
    print(f"phone_no: {phoneNumber}")
    print(f"text: {text}")
    phone_number: str = phoneNumber.replace("+", "")
    user = db.query(models.User).filter(
        models.User.phonenumber == phone_number).first()

    return await process_response(text, user=user)
