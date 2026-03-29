import httpx

LRCLIB_API_URL = "https://lrclib.net/api/get"


async def fetch_lyrics(title: str, artist: str) -> str | None:
    """Fetch plain lyrics from LRCLIB. Returns None if unavailable."""
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(
                LRCLIB_API_URL,
                params={"artist_name": artist, "track_name": title},
            )
            if response.status_code == 404:
                return None
            response.raise_for_status()
            data = response.json()
            return data.get("plainLyrics") or None
    except (httpx.HTTPError, KeyError, ValueError):
        return None
