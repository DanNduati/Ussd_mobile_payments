import httpx
from utils.lnm import generate_password
# post request

async def getAcessToken(url: str, consumer_key: str, consumer_secret: str):
    # make the request
    async with httpx.AsyncClient() as client:
        response = await client.get(url, auth=(consumer_key, consumer_secret))
        access_token = response.json()["access_token"]
    return access_token

async def initiate_payment(url: str, access_token: str, busines_shortcode: int, lnm_passkey: str, timestamp: str, amount: int, phone_number: int, callback_url: str):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    # json data
    payload = {
        "BusinessShortCode": busines_shortcode,
        "Password": generate_password(busines_shortcode, lnm_passkey),
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": phone_number,
        "PartyB": busines_shortcode,
        "PhoneNumber": phone_number,
        "CallBackURL": callback_url,
        "AccountReference": "CompanyXLTD",
        "TransactionDesc": "Payment of X"
    }

    async with httpx.AsyncClient() as client:
        r = await client.post(url, headers=headers, json=payload)
    return r.json()
