import datetime
from fastapi import APIRouter, BackgroundTasks, Form
from fastapi.responses import HTMLResponse
from typing import Optional
from ..schemas import UssdResponse
from fastapi.params import Depends
from sqlalchemy.orm import Session
from .. import models
from ..database import get_db
from ..services.lnm import send_stk

# create a simple callback url that prints out all ussd parameters from at
router = APIRouter(
    prefix="/ussd",
    tags=["Ussd callback"]
)


def generate_greeting():
    hour = datetime.datetime.now().hour
    greeting = "Good morning" if 5 <= hour < 12 else "Good afternoon" if hour < 18 else "Good evening"
    return greeting


def process_userinput(text: str) -> int:
    # This function process the text ussd parameter an return the menu level and user inputs
    # The output tuple is of the form => (menu level, [array of user inputs from the start of the session])
    return (len(text.split("*")), text.split("*"))


@router.post("/callback", response_class=HTMLResponse)
async def ussd_callback(background_tasks: BackgroundTasks, sessionId: str = Form(""), serviceCode: str = Form(""), phoneNumber=Form(""), text: Optional[str] = Form(""), db: Session = Depends(get_db)):
    # get user inside route
    print(f"session_id: {sessionId}")
    print(f"service_code: {serviceCode}")
    print(f"phone_no: {phoneNumber}")
    print(f"text: {text}")
    phone_number: str = phoneNumber.replace("+", "")
    user = db.query(models.User).filter(
        models.User.phonenumber == phone_number).first()
    resp: str = text
    response: str = ""
    enter_unitid: bool = False
    if process_userinput(resp)[0] == 1:
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
        else:
            response = "END Invalid option selected please try again!"
    elif process_userinput(resp)[0] == 2:
        # account selection menu
        if user:
            # check the number of accounts under the user to determine menu option length
            user_accounts = len(user.units)
            print(f"user has {user_accounts} accounts")
            # if the response is within this length the user is querying hi own accounts
            last_userinput = int(process_userinput(resp)[1][1])
            if last_userinput <= user_accounts and last_userinput != 0:
                # if the user has selected on of his accounts
                # get the account and query the balance
                acc_id = user.units[last_userinput-1].id
                # to do change this field name to balance
                acc_balance = user.units[last_userinput-1].value
                response += f"CON Your account balance for unitid{acc_id} is {acc_balance}\n"
                response += "1. pay via mpesa \n"
                response += "2. exit"
            else:
                # next option is entering unit id
                if last_userinput == user_accounts+1:
                    # set this flag to true if a registered user has opted to enter the unit id
                    enter_unitid = True
                    response += f"CON Please enter a valid unitid\n"
                    # followed by exit
                elif last_userinput == user_accounts+2:
                    response = "END Thank you for using this service!"
                else:
                    response = "END Invalid option selected please try again!"
        else:
            pass
    elif process_userinput(resp)[0] == 3:
        if user:
            if enter_unitid:
                # response for a user who opts to enter the id
                # get the entered id
                pass
            else:
                # response for user in payment menu there are only two options here pay and exit
                last_userinput = int(process_userinput(resp)[1][2])
                if last_userinput == 1:
                    background_tasks.add_task(send_stk, int(
                        user.units[last_userinput-1].value))
                    response += f"END Payment initiated check phone\n"
                elif last_userinput == 2:
                    response = "END Thank you for using this service!"
                else:
                    response = "END Invalid option selected please try again!"

        else:
            pass
    else:
        pass
    return response
