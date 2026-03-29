import httpx
from backend.config import settings
from backend.models.schemas import SpotifyTrackResponse

SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE = "https://api.spotify.com/v1"


class SpotifyClient:
    """Client for the Spotify Web API using Client Credentials flow."""

    def __init__(self) -> None:
        self._token: str | None = None

    async def get_track(self, spotify_url: str) -> SpotifyTrackResponse:
        """Fetch track metadata and audio features from a Spotify URL."""
        track_id = _extract_track_id(spotify_url)
        token = await self._get_token()

        async with httpx.AsyncClient(timeout=10) as client:
            try:
                track = await _fetch_track(client, track_id, token)
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 401:
                    # Token expired — refresh and retry
                    token = await self._refresh_token()
                    track = await _fetch_track(client, track_id, token)
                else:
                    raise
            features = await _fetch_audio_features(client, track_id, token)

        return _build_response(track, features)

    async def _get_token(self) -> str:
        """Fetch or return a cached Client Credentials access token."""
        if self._token:
            return self._token
        return await self._refresh_token()

    async def _refresh_token(self) -> str:
        """Fetch a fresh Client Credentials access token."""
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(
                SPOTIFY_TOKEN_URL,
                data={"grant_type": "client_credentials"},
                auth=(settings.spotify_client_id, settings.spotify_client_secret),
            )
            response.raise_for_status()
            self._token = response.json()["access_token"]
            return self._token


def _extract_track_id(url: str) -> str:
    """Parse a Spotify track ID from a full Spotify URL."""
    try:
        return url.split("/track/")[1].split("?")[0]
    except IndexError:
        raise ValueError(f"Could not parse track ID from URL: {url}")


async def _fetch_track(client: httpx.AsyncClient, track_id: str, token: str) -> dict:
    response = await client.get(
        f"{SPOTIFY_API_BASE}/tracks/{track_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    response.raise_for_status()
    return response.json()


async def _fetch_audio_features(
    client: httpx.AsyncClient, track_id: str, token: str
) -> dict | None:
    """Fetch audio features, returning None on failure (graceful fallback)."""
    try:
        response = await client.get(
            f"{SPOTIFY_API_BASE}/audio-features/{track_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        response.raise_for_status()
        return response.json()
    except httpx.HTTPError:
        return None


def _build_response(track: dict, features: dict | None) -> SpotifyTrackResponse:
    artist = track["artists"][0]["name"]
    genres: list[str] = track.get("album", {}).get("genres", [])
    fallback = features is None

    return SpotifyTrackResponse(
        title=track["name"],
        artist=artist,
        album=track["album"]["name"],
        genres=genres,
        energy=features.get("energy") if features else None,
        valence=features.get("valence") if features else None,
        tempo=features.get("tempo") if features else None,
        track_id=track["id"],
        fallback=fallback,
    )
