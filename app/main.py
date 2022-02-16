from fastapi import FastAPI
from accessToken import getAcessToken
from config import settings

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello There!"}


@app.get("/access_token")
async def Token() -> str:
    # make the request
    at = await getAcessToken(settings.accesstoken_url, settings.consumer_key, settings.consumer_secret)
    return at["access_token"]
