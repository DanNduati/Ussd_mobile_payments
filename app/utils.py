import asyncio
import httpx


async def getAcessToken(url: str, consumer_key: str, consumer_secret: str):
    # make the request
    async with httpx.AsyncClient() as client:
        r = await client.get(url, auth=(consumer_key, consumer_secret))
    return r.json()
