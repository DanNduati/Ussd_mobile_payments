from fastapi import FastAPI
from accessToken import getAcessToken
from stkpush import initiate_payment
from config import settings
from utils import get_timestamp, generate_password
from database import engine
import models

# create database tables
# ToDo : initialize database and run migrations with alembic instead
models.Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get("/")
async def root():
    print(generate_password(settings.business_shortcode, settings.lnm_passkey))
    return {"message": "Hello"}


@app.get("/stk_push")
async def stkPush():
    # get access token
    at = await getAcessToken(settings.accesstoken_url,
                             settings.consumer_key, settings.consumer_secret)
    # initate stkpush
    r = await initiate_payment(settings.lnm_url, at["access_token"], settings.business_shortcode, settings.lnm_passkey, get_timestamp(), 1, 254723060846, settings.lnm_callback_url)
    print("done")
    return r
