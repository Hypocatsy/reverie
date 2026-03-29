import logging
from fastapi import APIRouter, HTTPException
from backend.models.schemas import GenerateRequest, ErrorResponse, ImageRequest
from backend.providers import get_llm_provider, get_image_provider
from backend.providers.base import ProviderError
from backend.services.lyrics import fetch_lyrics

router = APIRouter(prefix="/api", tags=["generate"])
log = logging.getLogger("reverie.generate")


@router.post("/generate/prompt")
async def generate_prompt(request: GenerateRequest) -> dict:
    """Fetch lyrics and generate a visual prompt for the given song."""
    song = request.song
    log.info("Prompt generation requested: '%s' by %s", song.title, song.artist)

    lyrics = await fetch_lyrics(song.title, song.artist)
    if lyrics and lyrics.strip():
        song.lyrics = lyrics

    llm = get_llm_provider()
    try:
        visual_prompt = await llm.generate_visual_prompt(song)
    except ProviderError as e:
        log.error("LLM provider error: %s", e.message)
        raise HTTPException(status_code=502, detail=e.message)

    log.info("Visual prompt generated for '%s' by %s", song.title, song.artist)
    return {
        "visual_prompt": visual_prompt,
        "song_title": song.title,
        "artist": song.artist,
    }


@router.post("/generate/image")
async def generate_image_from_prompt(request: ImageRequest) -> dict:
    """Generate an image from a visual prompt."""
    log.info("Image generation requested")

    image = get_image_provider()
    try:
        image_url = await image.generate_image(request.visual_prompt)
    except ProviderError as e:
        log.error("Image provider error: %s", e.message)
        raise HTTPException(status_code=502, detail=e.message)

    log.info("Image generated successfully")
    return {"image_url": image_url}
