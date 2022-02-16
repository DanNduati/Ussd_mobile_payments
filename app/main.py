from fastapi import FastAPI
from utils import getAcessToken
from config import consumer_key, consumer_secret, accesstoken_url

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello There!"}


@app.get("/access_token")
async def Token() -> str:
    # make the request
    at = await getAcessToken(accesstoken_url, consumer_key, consumer_secret)
    return at["access_token"]
