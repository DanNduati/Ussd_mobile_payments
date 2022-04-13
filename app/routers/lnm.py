import json
from fastapi import APIRouter, Request
from pydantic import BaseModel, Json

router = APIRouter(
    prefix="/payments",
    tags=["Payment Callback"]
)


@router.post("/confirmation")
async def process_payment(request: Request):
    payment_response = await request.json()
    # print(payment_response)
    # serialize the callback response

    json_dump = json.dumps(payment_response, indent=4)
    json_object = json.loads(json_dump)
    # print(json_object["Body"]["stkCallback"]["ResultCode"])
    if json_object["Body"]["stkCallback"]["ResultCode"] == 0:
        # successful payment store payment data to file later db
        print(json_object["Body"]["stkCallback"]["ResultDesc"])
        with open("data/data.json", "w") as outfile:
            json.dump(payment_response, outfile)
    else:
        # unsuccessful payement Todo implement payment logging
        print(json_object["Body"]["stkCallback"]["ResultDesc"])
        with open("data/unsuccessful.json", "w") as outfile:
            json.dump(payment_response, outfile)
    return {"Message": "Callback received"}
