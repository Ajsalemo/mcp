# Constants
import asyncio
import logging
from typing import Any

import httpx

logging.basicConfig(level=logging.INFO)
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"


async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None


async def get_all_radar_stations() -> list[dict[str, Any]]:
    """Get all radar stations from the NWS API."""
    url = f"{NWS_API_BASE}/radar/stations"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return []

    logging.info(data)
    return data["features"]


if __name__ == "__main__":
    logging.info("t")
    asyncio.run(get_all_radar_stations())
