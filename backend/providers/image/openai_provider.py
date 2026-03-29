import logging
from openai import AsyncOpenAI
from backend.config import settings
from backend.providers.base import ImageProvider, ProviderError
from backend.services.image_store import save as store_image

log = logging.getLogger("reverie.provider.openai_image")


class OpenAIImageProvider(ImageProvider):
    """Image provider backed by OpenAI gpt-image-1."""

    def __init__(self) -> None:
        self._client = AsyncOpenAI(api_key=settings.openai_api_key)

    _style_prefix = (
        "Soft pastel illustration, clean line art, gentle whimsical storybook aesthetic,"
        " muted dreamy colours. NOT photorealistic, NOT a photograph. Hand-drawn feel.\n\n"
    )

    async def generate_image(self, prompt: str) -> str:
        try:
            styled_prompt = self._style_prefix + prompt
            response = await self._client.images.generate(
                model="gpt-image-1",
                prompt=styled_prompt,
                size="1024x1024",
                quality="low",
                n=1,
                response_format="b64_json",
            )
            b64 = response.data[0].b64_json
            if not b64:
                raise ProviderError("openai_image", "No image data returned from API")
            key = store_image(b64)
            return f"/api/image/generated/{key}"
        except ProviderError:
            raise
        except Exception as e:
            log.error("OpenAI image error: %s", e)
            raise ProviderError("openai_image", str(e))
