import urllib.parse
from backend.providers.base import ImageProvider, ProviderError

POLLINATIONS_IMAGE_BASE = "https://image.pollinations.ai/prompt"

STYLE_SUFFIX = (
    " Style: soft pastel illustration, clean line art, gentle whimsical storybook aesthetic,"
    " muted dreamy colours, no photorealism, no harsh lighting, no hyper-detail."
)


class PollinationsImageProvider(ImageProvider):
    """Image provider backed by the Pollinations image API (no key required)."""

    async def generate_image(self, prompt: str) -> str:
        try:
            styled_prompt = prompt.rstrip(". ") + "." + STYLE_SUFFIX
            encoded = urllib.parse.quote(styled_prompt)
            pollinations_url = (
                f"{POLLINATIONS_IMAGE_BASE}/{encoded}"
                f"?width=1024&height=1024&nologo=true&seed={_seed(prompt)}"
            )
            # Return via backend proxy — avoids browser CORS issues and
            # ensures the image URL is same-origin relative to the frontend.
            proxy_url = f"/api/image/proxy?url={urllib.parse.quote(pollinations_url)}"
            return proxy_url
        except Exception as e:
            raise ProviderError("pollinations_image", str(e))


def _seed(prompt: str) -> int:
    """Stable seed so the same prompt always returns the same image."""
    return abs(hash(prompt)) % 2**31
