import logging

import httpx

from backend.config import settings
from backend.providers.base import ImageProvider, ProviderError
from backend.services.image_store import save as store_image

log = logging.getLogger("reverie.provider.gemini")

GEMINI_API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"

_STYLE_PREFIX = (
    "Square 1:1 aspect ratio image. "
    "Soft pastel illustration, clean line art, gentle whimsical storybook aesthetic,"
    " muted dreamy colours. NOT photorealistic, NOT a photograph. Hand-drawn feel.\n\n"
)


class GeminiImageProvider(ImageProvider):
    """Image provider backed by the Google Gemini API."""

    async def generate_image(self, prompt: str) -> str:
        model = settings.gemini_model
        api_key = settings.gemini_api_key
        if not api_key:
            raise ProviderError("gemini_image", "GEMINI_API_KEY is not set")

        url = f"{GEMINI_API_BASE}/{model}:generateContent?key={api_key}"
        styled_prompt = _STYLE_PREFIX + prompt

        payload = {
            "contents": [{"parts": [{"text": styled_prompt}]}],
            "generationConfig": {
                "responseModalities": ["IMAGE", "TEXT"],
            },
        }

        try:
            async with httpx.AsyncClient(timeout=120) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                data = response.json()

            candidates = data.get("candidates", [])
            if not candidates:
                raise ProviderError("gemini_image", "No candidates in response")

            parts = candidates[0].get("content", {}).get("parts", [])

            # Find the image part in the response
            for part in parts:
                inline_data = part.get("inlineData")
                if inline_data and inline_data.get("data"):
                    b64 = inline_data["data"]
                    key = store_image(b64)
                    return f"/api/image/generated/{key}"

            raise ProviderError("gemini_image", "No image data in response")

        except ProviderError:
            raise
        except httpx.HTTPStatusError as e:
            body = e.response.text[:300]
            if settings.gemini_api_key:
                body = body.replace(settings.gemini_api_key, "[REDACTED]")
            log.error("Gemini HTTP %d: %s", e.response.status_code, body)
            raise ProviderError("gemini_image", f"HTTP {e.response.status_code}: {body}")
        except Exception as e:
            log.error("Gemini error: %s", e)
            raise ProviderError("gemini_image", str(e))
