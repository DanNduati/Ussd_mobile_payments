import httpx


async def getAcessToken(url: str, consumer_key: str, consumer_secret: str):
    # make the request
    async with httpx.AsyncClient() as client:
        response = await client.get(url, auth=(consumer_key, consumer_secret))
        access_token = response.json()["access_token"]
    return access_token
