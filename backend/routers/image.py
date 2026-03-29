import logging
import urllib.parse
import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse, Response
from backend.services.image_store import get as get_image

router = APIRouter(prefix="/api", tags=["image"])
log = logging.getLogger("reverie.image")

ALLOWED_HOST = "image.pollinations.ai"


@router.get("/image/proxy")
async def proxy_image(url: str) -> StreamingResponse:
    """Proxy an image from an allowed external host to avoid browser CORS issues."""
    parsed = urllib.parse.urlparse(url)
    if parsed.hostname != ALLOWED_HOST:
        log.warning("Blocked proxy request to disallowed host: %s", parsed.hostname)
        raise HTTPException(status_code=400, detail="Disallowed image host.")

    try:
        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.get(url)
            response.raise_for_status()
            content_type = response.headers.get("content-type", "image/jpeg")
            return StreamingResponse(
                iter([response.content]),
                media_type=content_type,
            )
    except httpx.HTTPError as e:
        log.error("Image proxy failed: %s", e)
        raise HTTPException(status_code=502, detail="Image could not be loaded.")


@router.get("/image/generated/{key}")
async def serve_generated_image(key: str) -> Response:
    """Serve a generated image from the in-memory store."""
    data = get_image(key)
    if data is None:
        log.warning("Image not found or expired: %s", key[:12])
        raise HTTPException(status_code=404, detail="Image not found or expired.")
    return Response(content=data, media_type="image/png")
