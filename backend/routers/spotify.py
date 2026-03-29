import logging
from fastapi import APIRouter, HTTPException, Query
from backend.models.schemas import SpotifyTrackResponse, ErrorResponse
from backend.services.spotify import SpotifyClient
from backend.config import settings

router = APIRouter(prefix="/api/spotify", tags=["spotify"])
log = logging.getLogger("reverie.spotify")
_client = SpotifyClient()


@router.get(
    "/track",
    response_model=SpotifyTrackResponse,
    responses={400: {"model": ErrorResponse}, 503: {"model": ErrorResponse}},
)
async def get_track(url: str = Query(..., description="Spotify track URL")) -> SpotifyTrackResponse:
    """Resolve a Spotify track URL to song metadata and audio features."""
    if not settings.spotify_enabled:
        raise HTTPException(status_code=503, detail="Spotify integration is disabled.")

    log.info("Resolving Spotify URL: %s", url[:80])
    try:
        result = await _client.get_track(url)
        log.info("Resolved: '%s' by %s", result.title, result.artist)
        return result
    except ValueError as e:
        log.warning("Invalid Spotify URL: %s — %s", url[:80], e)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        log.error("Spotify API error: %s", e)
        raise HTTPException(
            status_code=503,
            detail="Reverie couldn't reach Spotify right now — tell me about the song instead?",
        )
