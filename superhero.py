import httpx
from urllib.parse import quote

from config import SUPERHERO_API_TOKEN


async def search_superhero(name: str):
    url = (
        f"https://www.superheroapi.com/api/{SUPERHERO_API_TOKEN}/search/{quote(name)}"
    )

    async with httpx.AsyncClient(
        timeout=10,
        follow_redirects=True,
    ) as client:
        response = await client.get(url)
        response.raise_for_status()

    data = response.json()

    if data.get("response") != "success":
        return []

    return data.get("results", [])